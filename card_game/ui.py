"""
User Interface Module
Tkinter-based GUI for the party game.
UI logic is separated from game logic for reusability.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Callable
from game_logic import Game, Player
from scoreboard import Scoreboard


class GameUI:
    """Tkinter-based user interface for the party game."""

    def __init__(self, game: Game, scoreboard: Scoreboard):
        """
        Initialize the UI.

        Args:
            game (Game): Game instance.
            scoreboard (Scoreboard): Scoreboard instance.
        """
        self.game = game
        self.scoreboard = scoreboard
        self.root = tk.Tk()
        self.root.title("Juego de Preguntas para Fiestas")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        self.current_player_index = 0
        self.player_names = []
        self.game_active = False

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the initial UI with menu and main frame."""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo Juego", command=self.show_new_game_dialog)
        file_menu.add_command(label="Ver Marcador", command=self.show_scoreboard)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)

        # Main content frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Show welcome screen
        self.show_welcome_screen()

    def _clear_frame(self) -> None:
        """Clear all widgets from main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self) -> None:
        """Display welcome screen."""
        self._clear_frame()

        title = ttk.Label(
            self.main_frame,
            text="JUEGO DE PREGUNTAS PARA FIESTAS",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=30)

        rules_frame = ttk.LabelFrame(self.main_frame, text="REGLAS DEL JUEGO", padding=20)
        rules_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        rules_text = """
1. Cada jugador responde preguntas un turno por turno
2. Responde SI o NO a cada pregunta
3. IMPORTANTE: Solo recibes STRIKE si tu respuesta es CORRECTA
4. Maximo 3 strikes por jugador
5. Cuando llegues a 3 strikes: DEBES BEBER y los strikes se reinician
6. El ultimo jugador en pie gana
7. Presiona "Abandonar" para salir del juego en tu turno
        """

        rules_label = ttk.Label(rules_frame, text=rules_text, justify=tk.LEFT, font=("Arial", 10))
        rules_label.pack()

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        start_btn = ttk.Button(
            button_frame,
            text="Iniciar Juego",
            command=self.show_new_game_dialog,
            width=20
        )
        start_btn.pack(side=tk.LEFT, padx=5)

        exit_btn = ttk.Button(
            button_frame,
            text="Salir",
            command=self.root.quit,
            width=20
        )
        exit_btn.pack(side=tk.LEFT, padx=5)

    def show_new_game_dialog(self) -> None:
        """Show dialog to start a new game."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Juego")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Number of players
        ttk.Label(dialog, text="Numero de jugadores (2-10):", font=("Arial", 11)).pack(pady=10)
        num_players_var = tk.IntVar(value=2)
        num_players_spin = ttk.Spinbox(
            dialog,
            from_=2,
            to=10,
            textvariable=num_players_var,
            width=10
        )
        num_players_spin.pack(pady=5)

        # Player names frame
        players_frame = ttk.LabelFrame(dialog, text="Nombres de los jugadores", padding=10)
        players_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        entries = []

        def update_entries(*args):
            """Update entries based on spinbox value."""
            for entry in entries:
                entry.pack_forget()
            entries.clear()

            num = num_players_var.get()
            for i in range(num):
                ttk.Label(players_frame, text=f"Jugador {i + 1}:").pack()
                entry = ttk.Entry(players_frame, width=30)
                entry.pack(pady=5)
                entries.append(entry)

        num_players_var.trace("w", update_entries)
        update_entries()

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        def start_game():
            player_names = [entry.get().strip() for entry in entries]
            
            if not all(player_names):
                messagebox.showwarning("Error", "Todos los nombres son requeridos")
                return
            
            if len(set(player_names)) != len(player_names):
                messagebox.showwarning("Error", "Los nombres deben ser unicos")
                return

            self.player_names = player_names
            self.game.initialize_players(player_names)
            self.game.start_game()
            self.current_player_index = 0
            self.game_active = True
            dialog.destroy()
            self.show_game_screen()

        start_btn = ttk.Button(button_frame, text="Iniciar", command=start_game)
        start_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancelar", command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def show_game_screen(self) -> None:
        """Display the main game screen."""
        self._clear_frame()

        # Check game over
        if self.game.is_game_over():
            self.show_game_over()
            return

        # Get active players
        active_players = self.game.get_active_players()
        if len(active_players) <= 1:
            self.show_game_over()
            return

        # Check questions available
        if self.game.data_manager.get_unused_count() == 0:
            messagebox.showinfo("Fin del Juego", "No hay mas preguntas disponibles!")
            self.show_game_over()
            return

        # Get current player
        self.current_player_index = self.current_player_index % len(active_players)
        current_player = active_players[self.current_player_index]

        # Draw question
        question = self.game.draw_question()
        if not question:
            messagebox.showinfo("Fin del Juego", "No hay mas preguntas disponibles!")
            self.show_game_over()
            return

        # Header with game status
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=10)

        ttk.Label(
            header_frame,
            text=f"Ronda: {self.game.round_number}",
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)

        ttk.Label(
            header_frame,
            text=f"Jugadores activos: {len(active_players)}",
            font=("Arial", 12)
        ).pack(side=tk.RIGHT)

        # Current player status
        status_frame = ttk.LabelFrame(self.main_frame, text=f"Turno de: {current_player.name}", padding=10)
        status_frame.pack(fill=tk.X, pady=10)

        status = current_player.get_status()
        ttk.Label(
            status_frame,
            text=f"Strikes: {status['strikes']}/3",
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=20)
        ttk.Label(
            status_frame,
            text=f"Bebidas consumidas: {status['drinks_consumed']}",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=20)

        # Question section
        question_frame = ttk.LabelFrame(self.main_frame, text="PREGUNTA", padding=20)
        question_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        question_text = ttk.Label(
            question_frame,
            text=question['question'],
            font=("Arial", 13, "bold"),
            wraplength=700,
            justify=tk.CENTER
        )
        question_text.pack(pady=20)

        metadata = ttk.Label(
            question_frame,
            text=f"Categoria: {question['category']} | Dificultad: {question['difficulty']}/3",
            font=("Arial", 9)
        )
        metadata.pack()

        # Answer buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        def answer_yes():
            result = self.game.player_answers(current_player, answered_yes=True)
            self.show_answer_result(result, current_player)
            self.root.after(2000, self.next_turn)

        def answer_no():
            result = self.game.player_answers(current_player, answered_yes=False)
            self.show_answer_result(result, current_player)
            self.root.after(2000, self.next_turn)

        def clock_out():
            if messagebox.askyesno("Confirmar", f"{current_player.name} realmente desea abandonar el juego?"):
                self.game.player_clock_out(current_player)
                self.show_clock_out_message(current_player)
                self.root.after(2000, self.next_turn)

        yes_btn = ttk.Button(
            button_frame,
            text="SI",
            command=answer_yes,
            width=20
        )
        yes_btn.pack(side=tk.LEFT, padx=5)

        no_btn = ttk.Button(
            button_frame,
            text="NO",
            command=answer_no,
            width=20
        )
        no_btn.pack(side=tk.LEFT, padx=5)

        exit_btn = ttk.Button(
            button_frame,
            text="ABANDONAR",
            command=clock_out,
            width=20
        )
        exit_btn.pack(side=tk.LEFT, padx=5)

    def show_answer_result(self, result: dict, player: Player) -> None:
        """Display answer result."""
        self._clear_frame()

        if result['is_correct']:
            result_text = "RESPUESTA CORRECTA!"
            bg_color = "#90EE90"
        else:
            result_text = "RESPUESTA INCORRECTA"
            bg_color = "#FFB6C6"

        result_frame = tk.Frame(self.main_frame, bg=bg_color)
        result_frame.pack(fill=tk.X, padx=0, pady=0)

        result_label = tk.Label(
            result_frame,
            text=result_text,
            font=("Arial", 20, "bold"),
            bg=bg_color,
            pady=20
        )
        result_label.pack(fill=tk.X)

        info_frame = ttk.Frame(self.main_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        ttk.Label(
            info_frame,
            text=f"Jugador: {player.name}",
            font=("Arial", 12)
        ).pack()

        ttk.Label(
            info_frame,
            text=f"Respondiste: {'SI' if result['answered_yes'] else 'NO'}",
            font=("Arial", 12)
        ).pack()

        ttk.Label(
            info_frame,
            text=f"Respuesta correcta: {'SI' if result['correct_answer'] else 'NO'}",
            font=("Arial", 12)
        ).pack()

        ttk.Label(
            info_frame,
            text=f"Strikes actuales: {result['strikes']}/3",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        if result['must_drink']:
            ttk.Label(
                info_frame,
                text="DEBE BEBER! Strikes se reinician a 0",
                font=("Arial", 14, "bold"),
                foreground="red"
            ).pack(pady=10)

    def show_clock_out_message(self, player: Player) -> None:
        """Display clock out message."""
        self._clear_frame()

        ttk.Label(
            self.main_frame,
            text="FUERA DEL JUEGO!",
            font=("Arial", 20, "bold")
        ).pack(pady=30)

        ttk.Label(
            self.main_frame,
            text=f"{player.name} ha abandonado el juego",
            font=("Arial", 14)
        ).pack()

        ttk.Label(
            self.main_frame,
            text=f"Bebidas consumidas: {player.drinks_consumed}",
            font=("Arial", 12)
        ).pack(pady=20)

    def show_game_over(self) -> None:
        """Display game over screen."""
        self._clear_frame()
        self.game_active = False

        results = self.game.get_final_results()

        ttk.Label(
            self.main_frame,
            text="JUEGO TERMINADO!",
            font=("Arial", 18, "bold")
        ).pack(pady=30)

        results_frame = ttk.LabelFrame(self.main_frame, text="RESULTADOS FINALES", padding=20)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        ttk.Label(
            results_frame,
            text=f"GANADOR: {results['winner']}",
            font=("Arial", 14, "bold"),
            foreground="green"
        ).pack(pady=10)

        ttk.Label(
            results_frame,
            text=f"PERDEDOR: {results['loser']}",
            font=("Arial", 12),
            foreground="red"
        ).pack()

        standings_frame = ttk.LabelFrame(results_frame, text="Clasificacion", padding=10)
        standings_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        for standing in results['standings']:
            text = f"{standing['rank']}. {standing['name']}: {standing['drinks']} bebida(s), {standing['strikes']} strikes"
            ttk.Label(standings_frame, text=text, font=("Arial", 10)).pack()

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        play_again_btn = ttk.Button(
            button_frame,
            text="Jugar Nuevamente",
            command=self.show_new_game_dialog,
            width=20
        )
        play_again_btn.pack(side=tk.LEFT, padx=5)

        menu_btn = ttk.Button(
            button_frame,
            text="Menu Principal",
            command=self.show_welcome_screen,
            width=20
        )
        menu_btn.pack(side=tk.LEFT, padx=5)

    def next_turn(self) -> None:
        """Move to next turn."""
        self.current_player_index += 1
        self.show_game_screen()

    def show_scoreboard(self) -> None:
        """Show scoreboard window."""
        scoreboard_window = tk.Toplevel(self.root)
        scoreboard_window.title("Marcador")
        scoreboard_window.geometry("500x400")

        summary = self.scoreboard.get_summary()

        ttk.Label(
            scoreboard_window,
            text="MARCADOR DEL JUEGO",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        summary_frame = ttk.LabelFrame(scoreboard_window, text="Resumen", padding=10)
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(
            summary_frame,
            text=f"Total eventos: {summary['total_events']}",
            font=("Arial", 10)
        ).pack()

        ttk.Label(
            summary_frame,
            text=f"Eventos de strike: {summary['total_strike_events']}",
            font=("Arial", 10)
        ).pack()

        ttk.Label(
            summary_frame,
            text=f"Eventos de bebida: {summary['total_drinking_events']}",
            font=("Arial", 10)
        ).pack()

    def show_about(self) -> None:
        """Show about dialog."""
        messagebox.showinfo(
            "Acerca de",
            "Juego de Preguntas para Fiestas\n\n"
            "Un juego divertido para fiestas\n\n"
            "Version 1.0"
        )

    def run(self) -> None:
        """Run the application."""
        self.root.mainloop()
