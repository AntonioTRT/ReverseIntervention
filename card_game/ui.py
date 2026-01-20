"""
User Interface Module
PyQt5-based GUI for the party game.
UI logic is separated from game logic for reusability.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSpinBox, QLineEdit, 
                             QDialog, QMessageBox, QScrollArea, QFrame,
                             QGroupBox, QGridLayout, QStackedWidget)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import QSize
from game_logic import Game, Player
from scoreboard import Scoreboard


class WelcomeScreen(QWidget):
    """Welcome screen widget."""
    
    def __init__(self, parent=None):
        """Initialize welcome screen."""
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """Set up the welcome screen UI."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("PARTY TRIVIA GAME")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(title)
        layout.addSpacing(20)
        
        # Rules
        rules_label = QLabel("GAME RULES")
        rules_font = QFont()
        rules_font.setPointSize(12)
        rules_font.setBold(True)
        rules_label.setFont(rules_font)
        rules_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(rules_label)
        
        rules_text = """
1. Each player answers questions one turn at a time
2. Answer YES or NO to each question
3. IMPORTANT: You receive a STRIKE only if you answer YES
4. Maximum 3 strikes per player
5. When you reach 3 strikes: YOU MUST DRINK and strikes reset
6. The last player standing wins
7. Press "Quit" to leave the game during your turn
        """
        
        rules = QLabel(rules_text)
        rules.setAlignment(Qt.AlignLeft)
        rules_font.setPointSize(10)
        rules_font.setBold(False)
        rules.setFont(rules_font)
        layout.addWidget(rules)
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        start_btn = QPushButton("Start Game")
        start_btn.setMinimumWidth(150)
        start_btn.setMinimumHeight(40)
        start_btn.clicked.connect(self.parent_window.show_new_game_dialog)
        button_layout.addWidget(start_btn)
        
        exit_btn = QPushButton("Exit")
        exit_btn.setMinimumWidth(150)
        exit_btn.setMinimumHeight(40)
        exit_btn.clicked.connect(self.parent_window.close)
        button_layout.addWidget(exit_btn)
        
        button_layout.addStretch()
        layout.addSpacing(20)
        layout.addLayout(button_layout)
        layout.addSpacing(20)
        
        self.setLayout(layout)


class GameUI(QMainWindow):
    """Main window for the party game."""
    
    def __init__(self, game, scoreboard):
        """Initialize the main window."""
        super().__init__()
        self.game = game
        self.scoreboard = scoreboard
        self.result_timer = QTimer()
        self.result_timer.timeout.connect(self.next_turn)
        
        self.setWindowTitle("Party Trivia Game")
        self.setGeometry(100, 100, 900, 700)
        
        # Create menu bar
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        new_game_action = file_menu.addAction("New Game")
        new_game_action.triggered.connect(self.show_new_game_dialog)
        
        scoreboard_action = file_menu.addAction("View Scoreboard")
        scoreboard_action.triggered.connect(self.show_scoreboard)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
        # Central widget - stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Show welcome screen
        welcome = WelcomeScreen(self)
        self.stacked_widget.addWidget(welcome)
        self.stacked_widget.setCurrentWidget(welcome)
    
    def show_new_game_dialog(self):
        """Show dialog to create new game."""
        dialog = QDialog(self)
        dialog.setWindowTitle("New Game")
        dialog.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        
        # Number of players
        num_label = QLabel("Number of Players (2-10):")
        layout.addWidget(num_label)
        
        num_spinbox = QSpinBox()
        num_spinbox.setMinimum(2)
        num_spinbox.setMaximum(10)
        num_spinbox.setValue(2)
        layout.addWidget(num_spinbox)
        
        layout.addSpacing(15)
        
        # Player names
        names_label = QLabel("Player Names:")
        names_label_font = QFont()
        names_label_font.setBold(True)
        names_label.setFont(names_label_font)
        layout.addWidget(names_label)
        
        entries = []
        entry_layouts = []
        
        def update_entries(value):
            """Update entries based on spinbox value."""
            # Delete all previous entries and their layouts
            for entry in entries:
                entry.deleteLater()
            entries.clear()
            
            for entry_layout in entry_layouts:
                # Remove all widgets from the layout first
                while entry_layout.count():
                    item = entry_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                entry_layout.deleteLater()
            entry_layouts.clear()
            
            # Create new entries
            for i in range(value):
                label = QLabel(f"Player {i + 1}:")
                entry = QLineEdit()
                entry.setText(f"Player {i + 1}")  # Set default name
                entries.append(entry)
                
                entry_layout = QHBoxLayout()
                entry_layout.addWidget(label)
                entry_layout.addWidget(entry)
                entry_layouts.append(entry_layout)
                layout.insertLayout(layout.count() - 1, entry_layout)
        
        num_spinbox.valueChanged.connect(update_entries)
        update_entries(2)
        
        layout.addSpacing(15)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        def start_game():
            player_names = [entry.text().strip() for entry in entries]
            
            if not all(player_names):
                QMessageBox.warning(dialog, "Error", "All player names are required")
                return
            
            if len(set(player_names)) != len(player_names):
                QMessageBox.warning(dialog, "Error", "Player names must be unique")
                return
            
            self.game.initialize_players(player_names)
            self.game.start_game()
            dialog.accept()
            self.show_game_screen()
        
        start_btn = QPushButton("Start")
        start_btn.clicked.connect(start_game)
        button_layout.addWidget(start_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def setup_new_turn(self):
        """Setup a new turn with a new question for the current player."""
        active_players = self.game.get_active_players()
        
        # Check game state
        if self.game.is_game_over() or len(active_players) <= 1 or self.game.data_manager.get_unused_count() == 0:
            self.show_game_over()
            return False
        
        # Move to next player in rotation
        if self.game.current_player_index is None:
            self.game.current_player_index = 0
        else:
            self.game.current_player_index += 1
        
        # Reset current question for new turn
        self.game.current_question = None
        
        # Draw question for this turn
        question = self.game.draw_question()
        if not question:
            self.show_game_over()
            return False
        
        return True
    
    def create_all_players_scoreboard(self, current_player=None):
        """Create a scoreboard widget showing all players' strikes.
        
        Args:
            current_player (Player): The player whose turn it is (will be highlighted).
            
        Returns:
            QGroupBox: A group box containing the scoreboard.
        """
        all_players = self.game.players
        
        scoreboard_frame = QGroupBox("Players Scoreboard")
        scoreboard_layout = QGridLayout()
        
        # Header
        name_header = QLabel("Player")
        name_header_font = QFont()
        name_header_font.setBold(True)
        name_header.setFont(name_header_font)
        scoreboard_layout.addWidget(name_header, 0, 0)
        
        strikes_header = QLabel("Strikes")
        strikes_header.setFont(name_header_font)
        scoreboard_layout.addWidget(strikes_header, 0, 1)
        
        drinks_header = QLabel("Drinks")
        drinks_header.setFont(name_header_font)
        scoreboard_layout.addWidget(drinks_header, 0, 2)
        
        status_header = QLabel("Status")
        status_header.setFont(name_header_font)
        scoreboard_layout.addWidget(status_header, 0, 3)
        
        # Add each player
        for idx, player in enumerate(all_players, 1):
            # Player name (highlighted ONLY if it's current player's turn)
            name_label = QLabel(player.name)
            name_font = QFont()
            name_font.setPointSize(10)
            
            if current_player and player == current_player:
                name_font.setBold(True)
                name_label.setStyleSheet("background-color: yellow; color: black; font-weight: bold; padding: 2px;")
            elif not player.is_active:
                name_label.setStyleSheet("color: gray; text-decoration: line-through;")
            
            name_label.setFont(name_font)
            scoreboard_layout.addWidget(name_label, idx, 0)
            
            # Strikes
            strikes_label = QLabel(f"{player.strikes}/3")
            strikes_label.setFont(name_font)
            scoreboard_layout.addWidget(strikes_label, idx, 1)
            
            # Drinks
            drinks_label = QLabel(str(player.drinks_consumed))
            drinks_label.setFont(name_font)
            scoreboard_layout.addWidget(drinks_label, idx, 2)
            
            # Status
            if not player.is_active:
                status_text = "Out"
                status_label = QLabel(status_text)
                status_label.setStyleSheet("color: red;")
            else:
                status_label = QLabel("Active")
                status_label.setStyleSheet("color: green;")
            
            status_label.setFont(name_font)
            scoreboard_layout.addWidget(status_label, idx, 3)
        
        scoreboard_frame.setLayout(scoreboard_layout)
        return scoreboard_frame
    
    def show_game_screen(self):
        """Show game screen - main game UI that updates in place."""
        # Check game state
        if self.game.is_game_over():
            self.show_game_over()
            return
        
        active_players = self.game.get_active_players()
        if len(active_players) <= 1 or self.game.data_manager.get_unused_count() == 0:
            self.show_game_over()
            return
        
        # Setup new turn if needed
        if not self.setup_new_turn():
            return
        
        # Clear all previous game screens from stacked widget (keep only welcome)
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        # Create main game widget
        game_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Get current player based on active players index
        # Map the absolute player index to the active players list
        current_player_idx = self.game.current_player_index % len(active_players)
        current_player = active_players[current_player_idx]
        
        question = self.game.current_question
        
        # Header
        header_layout = QHBoxLayout()
        
        ronda_label = QLabel(f"Ronda: {self.game.round_number}")
        ronda_font = QFont()
        ronda_font.setPointSize(12)
        ronda_font.setBold(True)
        ronda_label.setFont(ronda_font)
        header_layout.addWidget(ronda_label)
        
        jugadores_label = QLabel(f"Jugadores activos: {len(active_players)}")
        jugadores_label.setFont(ronda_font)
        header_layout.addStretch()
        header_layout.addWidget(jugadores_label)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Player status frame
        status_frame = QGroupBox(f"Turn: {current_player.name}")
        status_layout = QHBoxLayout()
        
        status = current_player.get_status()
        strikes_label = QLabel(f"Strikes: {status['strikes']}/3")
        strikes_font = QFont()
        strikes_font.setPointSize(11)
        strikes_font.setBold(True)
        strikes_label.setFont(strikes_font)
        status_layout.addWidget(strikes_label)
        
        drinks_label = QLabel(f"Drinks Consumed: {status['drinks_consumed']}")
        drinks_label.setFont(strikes_font)
        status_layout.addStretch()
        status_layout.addWidget(drinks_label)
        
        status_frame.setLayout(status_layout)
        main_layout.addWidget(status_frame)
        main_layout.addSpacing(20)
        
        # Question frame
        question_frame = QGroupBox("QUESTION")
        question_layout = QVBoxLayout()
        
        question_text = QLabel(question['question'])
        question_font = QFont()
        question_font.setPointSize(13)
        question_font.setBold(True)
        question_text.setFont(question_font)
        question_text.setAlignment(Qt.AlignCenter)
        question_text.setWordWrap(True)
        question_layout.addWidget(question_text)
        
        question_layout.addSpacing(15)
        
        metadata = QLabel(f"Category: {question['category']} | Difficulty: {question['difficulty']}/3")
        metadata_font = QFont()
        metadata_font.setPointSize(9)
        metadata.setFont(metadata_font)
        metadata.setAlignment(Qt.AlignCenter)
        question_layout.addWidget(metadata)
        
        question_frame.setLayout(question_layout)
        main_layout.addWidget(question_frame)
        
        main_layout.addSpacing(20)
        
        # Add all players scoreboard (persistent)
        scoreboard_widget = self.create_all_players_scoreboard(current_player)
        main_layout.addWidget(scoreboard_widget)
        
        main_layout.addSpacing(20)
        
        # Answer buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        def answer_yes():
            result = self.game.player_answers(current_player, answered_yes=True)
            self.show_answer_result(result, current_player)
        
        def answer_no():
            result = self.game.player_answers(current_player, answered_yes=False)
            self.show_answer_result(result, current_player)
        
        def clock_out():
            reply = QMessageBox.question(
                self, "Confirm",
                f"Are you sure {current_player.name} wants to quit the game?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.game.player_clock_out(current_player)
                self.show_clock_out_message(current_player)
        
        yes_btn = QPushButton("YES")
        yes_btn.setMinimumHeight(50)
        yes_btn.setMinimumWidth(150)
        yes_font = QFont()
        yes_font.setPointSize(12)
        yes_font.setBold(True)
        yes_btn.setFont(yes_font)
        yes_btn.clicked.connect(answer_yes)
        button_layout.addWidget(yes_btn)
        
        no_btn = QPushButton("NO")
        no_btn.setMinimumHeight(50)
        no_btn.setMinimumWidth(150)
        no_btn.setFont(yes_font)
        no_btn.clicked.connect(answer_no)
        button_layout.addWidget(no_btn)
        
        exit_btn = QPushButton("QUIT")
        exit_btn.setMinimumHeight(50)
        exit_btn.setMinimumWidth(150)
        exit_btn.setFont(yes_font)
        exit_btn.clicked.connect(clock_out)
        button_layout.addWidget(exit_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        game_widget.setLayout(main_layout)
        
        self.stacked_widget.addWidget(game_widget)
        self.stacked_widget.setCurrentWidget(game_widget)
    
    def show_answer_result(self, result, player):
        """Show answer result by clearing and rebuilding entire screen."""
        # Stop the timer to prevent race conditions
        self.result_timer.stop()
        
        # Clear the stacked widget - remove game screen
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
        
        # Create new result screen
        result_widget = QWidget()
        result_main_layout = QVBoxLayout()
        
        active_players = self.game.get_active_players()
        
        # Header
        header_layout = QHBoxLayout()
        
        ronda_label = QLabel(f"Round: {self.game.round_number}")
        ronda_font = QFont()
        ronda_font.setPointSize(12)
        ronda_font.setBold(True)
        ronda_label.setFont(ronda_font)
        header_layout.addWidget(ronda_label)
        
        jugadores_label = QLabel(f"Active Players: {len(active_players)}")
        jugadores_label.setFont(ronda_font)
        header_layout.addStretch()
        header_layout.addWidget(jugadores_label)
        
        result_main_layout.addLayout(header_layout)
        result_main_layout.addSpacing(10)
        
        # Player status frame
        status_frame = QGroupBox(f"Turn: {player.name}")
        status_layout = QHBoxLayout()
        
        status = player.get_status()
        strikes_label = QLabel(f"Strikes: {status['strikes']}/3")
        strikes_font = QFont()
        strikes_font.setPointSize(11)
        strikes_font.setBold(True)
        strikes_label.setFont(strikes_font)
        status_layout.addWidget(strikes_label)
        
        drinks_label = QLabel(f"Drinks Consumed: {status['drinks_consumed']}")
        drinks_label.setFont(strikes_font)
        status_layout.addStretch()
        status_layout.addWidget(drinks_label)
        
        status_frame.setLayout(status_layout)
        result_main_layout.addWidget(status_frame)
        result_main_layout.addSpacing(20)
        
        # Result header - show strike result based on YES/NO answer
        if result['answered_yes']:
            result_text = "STRIKE RECEIVED!"
            color = "#FFB6C6"
        else:
            result_text = "NO STRIKE"
            color = "#90EE90"
        
        result_frame = QFrame()
        result_frame.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
        result_layout = QVBoxLayout()
        
        result_label = QLabel(result_text)
        result_font = QFont()
        result_font.setPointSize(18)
        result_font.setBold(True)
        result_label.setFont(result_font)
        result_label.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(result_label)
        
        result_frame.setLayout(result_layout)
        result_main_layout.addWidget(result_frame)
        result_main_layout.addSpacing(20)
        
        # Info
        info_layout = QVBoxLayout()
        
        jugador_label = QLabel(f"Player: {player.name}")
        jugador_font = QFont()
        jugador_font.setPointSize(11)
        jugador_label.setFont(jugador_font)
        info_layout.addWidget(jugador_label)
        
        respondiste_label = QLabel(f"You answered: {'YES' if result['answered_yes'] else 'NO'}")
        respondiste_label.setFont(jugador_font)
        info_layout.addWidget(respondiste_label)
        
        strikes_label = QLabel(f"Current Strikes: {result['strikes']}/3")
        strikes_font = QFont()
        strikes_font.setPointSize(12)
        strikes_font.setBold(True)
        strikes_label.setFont(strikes_font)
        info_layout.addWidget(strikes_label)
        info_layout.addSpacing(10)
        
        if result['must_drink']:
            beber_label = QLabel("YOU MUST DRINK! Strikes reset to 0")
            beber_font = QFont()
            beber_font.setPointSize(13)
            beber_font.setBold(True)
            beber_label.setFont(beber_font)
            beber_label.setStyleSheet("color: red;")
            info_layout.addWidget(beber_label)
        
        result_main_layout.addLayout(info_layout)
        result_main_layout.addSpacing(20)
        
        # Add all players scoreboard (persistent)
        scoreboard_widget = self.create_all_players_scoreboard(player)
        result_main_layout.addWidget(scoreboard_widget)
        
        result_main_layout.addStretch()
        
        result_widget.setLayout(result_main_layout)
        self.stacked_widget.addWidget(result_widget)
        self.stacked_widget.setCurrentWidget(result_widget)
        
        # Restart timer to go to next turn
        self.result_timer.start(2000)
    
    def show_clock_out_message(self, player):
        """Show clock out message by clearing and rebuilding entire screen."""
        # Stop the timer to prevent race conditions
        self.result_timer.stop()
        
        # Clear the stacked widget - remove game screen
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
        
        # Create new clock out screen
        clock_out_widget = QWidget()
        clock_out_layout = QVBoxLayout()
        
        active_players = self.game.get_active_players()
        
        # Header
        header_layout = QHBoxLayout()
        
        ronda_label = QLabel(f"Ronda: {self.game.round_number}")
        ronda_font = QFont()
        ronda_font.setPointSize(12)
        ronda_font.setBold(True)
        ronda_label.setFont(ronda_font)
        header_layout.addWidget(ronda_label)
        
        jugadores_label = QLabel(f"Jugadores activos: {len(active_players)}")
        jugadores_label.setFont(ronda_font)
        header_layout.addStretch()
        header_layout.addWidget(jugadores_label)
        
        clock_out_layout.addLayout(header_layout)
        clock_out_layout.addSpacing(10)
        
        # Player status frame
        status_frame = QGroupBox("Game Status")
        status_layout = QHBoxLayout()
        status_layout.addStretch()
        
        status_text = QLabel("Processing...")
        status_text.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        
        status_frame.setLayout(status_layout)
        clock_out_layout.addWidget(status_frame)
        clock_out_layout.addSpacing(50)
        
        titulo = QLabel("PLAYER OUT!")
        titulo_font = QFont()
        titulo_font.setPointSize(18)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        clock_out_layout.addWidget(titulo)
        clock_out_layout.addSpacing(20)
        
        mensaje = QLabel(f"{player.name} has quit the game")
        mensaje_font = QFont()
        mensaje_font.setPointSize(13)
        mensaje.setFont(mensaje_font)
        mensaje.setAlignment(Qt.AlignCenter)
        clock_out_layout.addWidget(mensaje)
        
        bebidas = QLabel(f"Drinks Consumed: {player.drinks_consumed}")
        bebidas.setFont(mensaje_font)
        bebidas.setAlignment(Qt.AlignCenter)
        clock_out_layout.addWidget(bebidas)
        
        clock_out_layout.addSpacing(20)
        
        # Add all players scoreboard (persistent)
        scoreboard_widget = self.create_all_players_scoreboard()
        clock_out_layout.addWidget(scoreboard_widget)
        
        clock_out_layout.addStretch()
        
        clock_out_widget.setLayout(clock_out_layout)
        self.stacked_widget.addWidget(clock_out_widget)
        self.stacked_widget.setCurrentWidget(clock_out_widget)
        
        # Restart timer to go to next turn
        self.result_timer.start(2000)
    
    def next_turn(self):
        """Move to next turn."""
        self.result_timer.stop()
        active_players = self.game.get_active_players()
        
        # Check if game is over
        if self.game.is_game_over():
            self.show_game_over()
            return
        
        # Check if no more questions
        if self.game.data_manager.get_unused_count() == 0:
            self.show_game_over()
            return
        
        # Show next turn (setup_new_turn will increment the player index)
        self.show_game_screen()
    
    def show_game_over(self):
        """Show game over screen."""
        # Remove all stacked widgets except welcome
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
        
        results = self.game.get_final_results()
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        titulo = QLabel("GAME OVER!")
        titulo_font = QFont()
        titulo_font.setPointSize(18)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        layout.addSpacing(20)
        
        # Results frame
        results_frame = QGroupBox("FINAL RESULTS")
        results_layout = QVBoxLayout()
        
        ganador = QLabel(f"WINNER: {results['winner']}")
        ganador_font = QFont()
        ganador_font.setPointSize(12)
        ganador_font.setBold(True)
        ganador.setFont(ganador_font)
        ganador.setStyleSheet("color: green;")
        results_layout.addWidget(ganador)
        
        perdedor = QLabel(f"LOSER: {results['loser']}")
        perdedor_font = QFont()
        perdedor_font.setPointSize(11)
        perdedor.setFont(perdedor_font)
        perdedor.setStyleSheet("color: red;")
        results_layout.addWidget(perdedor)
        
        results_layout.addSpacing(15)
        
        clasificacion = QLabel("Rankings:")
        clasificacion_font = QFont()
        clasificacion_font.setBold(True)
        clasificacion.setFont(clasificacion_font)
        results_layout.addWidget(clasificacion)
        
        for standing in results['standings']:
            text = f"{standing['rank']}. {standing['name']}: {standing['drinks']} drink(s), {standing['strikes']} strikes"
            standing_label = QLabel(text)
            results_layout.addWidget(standing_label)
        
        results_frame.setLayout(results_layout)
        layout.addWidget(results_frame)
        layout.addSpacing(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        play_again_btn = QPushButton("Play Again")
        play_again_btn.setMinimumHeight(40)
        play_again_btn.setMinimumWidth(150)
        play_again_btn.clicked.connect(self.show_new_game_dialog)
        button_layout.addWidget(play_again_btn)
        
        menu_btn = QPushButton("Main Menu")
        menu_btn.setMinimumHeight(40)
        menu_btn.setMinimumWidth(150)
        menu_btn.clicked.connect(self.back_to_welcome)
        button_layout.addWidget(menu_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)
    
    def back_to_welcome(self):
        """Go back to welcome screen."""
        # Reset game
        self.game.data_manager.reset_all_questions()
        self.game.players = []
        self.game.current_player_index = 0
        self.game.round_number = 0
        self.game.is_started = False
        
        # Remove all stacked widgets except welcome
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
        
        # Show welcome
        self.stacked_widget.setCurrentIndex(0)
    
    def show_scoreboard(self):
        """Show scoreboard window."""
        summary = self.scoreboard.get_summary()
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Marcador")
        dialog.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        titulo = QLabel("MARCADOR DEL JUEGO")
        titulo_font = QFont()
        titulo_font.setPointSize(13)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        layout.addSpacing(10)
        
        summary_frame = QGroupBox("Resumen")
        summary_layout = QVBoxLayout()
        
        total_label = QLabel(f"Total eventos: {summary['total_events']}")
        summary_layout.addWidget(total_label)
        
        strikes_label = QLabel(f"Eventos de strike: {summary['total_strike_events']}")
        summary_layout.addWidget(strikes_label)
        
        drinks_label = QLabel(f"Eventos de bebida: {summary['total_drinking_events']}")
        summary_layout.addWidget(drinks_label)
        
        summary_frame.setLayout(summary_layout)
        layout.addWidget(summary_frame)
        layout.addStretch()
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.information(
            self,
            "Acerca de",
            "Juego de Preguntas para Fiestas\n\n"
            "Un juego divertido para fiestas\n\n"
            "Version 2.0"
        )
    
    def run(self):
        """Run the application."""
        self.show()
