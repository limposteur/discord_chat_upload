"""
Telecharge les messages d'un salon Discord via DiscordChatExporter CLI.
Telecharge DCE : https://github.com/Tyrrrz/DiscordChatExporter/releases
  -> DiscordChatExporter.Cli.zip (Windows x64)
"""
import subprocess
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Discord Channel Exporter")
        self.root.geometry("600x480")
        self.root.resizable(True, True)
        self._process: subprocess.Popen | None = None
        self._running = False
        self._build_ui()

    def _build_ui(self):
        f = ttk.Frame(self.root, padding=14)
        f.pack(fill="both", expand=True)

        # DCE path
        ttk.Label(f, text="DiscordChatExporter.Cli.exe :").grid(row=0, column=0, columnspan=2, sticky="w")
        row0 = ttk.Frame(f)
        row0.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 8))
        self.cli_var = tk.StringVar()
        ttk.Entry(row0, textvariable=self.cli_var, width=56).pack(side="left", fill="x", expand=True)
        ttk.Button(row0, text="…", width=3, command=self._browse).pack(side="left", padx=(4, 0))

        # Token
        ttk.Label(f, text="Token Discord (compte perso) :").grid(row=2, column=0, columnspan=2, sticky="w")
        self.token_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.token_var, show="*").grid(row=3, column=0, columnspan=2, sticky="ew", pady=(2, 8))

        # Channel ID
        ttk.Label(f, text="Channel ID :").grid(row=4, column=0, columnspan=2, sticky="w")
        self.channel_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.channel_var).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(2, 10))

        # Buttons
        btn_row = ttk.Frame(f)
        btn_row.grid(row=6, column=0, columnspan=2, sticky="w")
        self.start_btn = ttk.Button(btn_row, text="Télécharger", command=self._start)
        self.start_btn.pack(side="left")
        self.stop_btn = ttk.Button(btn_row, text="Stop (sauvegarde)", command=self._stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(8, 0))
        ttk.Button(btn_row, text="Quitter", command=self._kill).pack(side="left", padx=(8, 0))

        # Status
        self.status_var = tk.StringVar(value="Prêt")
        ttk.Label(f, textvariable=self.status_var, foreground="#555").grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 4))

        # Log
        ttk.Label(f, text="Logs :").grid(row=8, column=0, columnspan=2, sticky="w")
        log_frame = ttk.Frame(f)
        log_frame.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=(2, 0))
        vsb = ttk.Scrollbar(log_frame)
        vsb.pack(side="right", fill="y")
        self.log = tk.Text(log_frame, height=12, state="disabled", font=("Consolas", 9),
                           bg="#1e1e1e", fg="#d4d4d4", yscrollcommand=vsb.set, wrap="word")
        self.log.pack(fill="both", expand=True)
        vsb.config(command=self.log.yview)

        f.columnconfigure(0, weight=1)
        f.rowconfigure(9, weight=1)

    # ---------------------------------------------------------------- actions

    def _browse(self):
        p = filedialog.askopenfilename(title="DiscordChatExporter.Cli.exe",
                                       filetypes=[("Executable", "*.exe"), ("All", "*.*")])
        if p:
            self.cli_var.set(p)

    def _start(self):
        cli = self.cli_var.get().strip()
        token = self.token_var.get().strip()
        channel = self.channel_var.get().strip()

        if not cli or not Path(cli).exists():
            messagebox.showerror("Erreur", "Chemin vers DiscordChatExporter.Cli.exe invalide.")
            return
        if not token:
            messagebox.showerror("Erreur", "Entre ton token Discord.")
            return
        if not channel.isdigit():
            messagebox.showerror("Erreur", "Le Channel ID doit contenir uniquement des chiffres.")
            return

        self._log_clear()
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_var.set("Téléchargement en cours…")
        self._running = True

        threading.Thread(target=self._run, args=(cli, token, channel), daemon=True).start()

    def _stop(self):
        if self._process and self._running:
            self._log_append("[STOP] Arrêt demandé — sauvegarde ce qui a été téléchargé…\n")
            self._process.terminate()

    def _kill(self):
        if self._process:
            self._process.kill()
        self.root.destroy()

    # ---------------------------------------------------------------- worker

    def _run(self, cli: str, token: str, channel: str):
        output_dir = Path.cwd() / "exports"
        output_dir.mkdir(exist_ok=True)

        cmd = [cli, "export", "-t", token, "--bot", "false",
               "-c", channel, "-o", str(output_dir), "--format", "Json"]

        self._log_append(f"Commande : {' '.join(cmd)}\n\n")

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            # Lire ligne par ligne sans bloquer l'UI
            for line in self._process.stdout:
                if not self._running:
                    break
                self._log_append(line)

            self._process.wait()
            returncode = self._process.returncode

        except Exception as exc:
            self._log_append(f"\nERREUR : {exc}\n")
            returncode = -1
        finally:
            self._running = False
            self._process = None

        # Chercher le fichier produit même en cas de stop
        files = sorted(output_dir.glob(f"*{channel}*.json"))
        if not files:
            files = sorted(output_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

        if files:
            result = f"Fichier : {files[0]}"
            self.root.after(0, lambda p=str(files[0]): messagebox.showinfo("Terminé", f"Export sauvegardé.\n{p}"))
        elif returncode == 0:
            result = f"Terminé (voir {output_dir})"
        else:
            result = "Arrêté ou erreur"

        self.root.after(0, lambda r=result: self.status_var.set(r))
        self.root.after(0, lambda: self.start_btn.config(state="normal"))
        self.root.after(0, lambda: self.stop_btn.config(state="disabled"))

    # ---------------------------------------------------------------- logging

    def _log_append(self, text: str):
        self.root.after(0, self._write_log, text)

    def _write_log(self, text: str):
        self.log.config(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.config(state="disabled")

    def _log_clear(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
