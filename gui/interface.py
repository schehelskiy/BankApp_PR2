import customtkinter as ctk
from models.core import UserRole, Transaction
from models.auth import AuthManager
from models.utils import generate_id
from models.database import Database
from datetime import datetime

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Елітна Банківська Система")
        self.root.geometry("900x700")
        self.db = Database()
        self.auth = AuthManager(self.db)
        self.current_frame = None
        self.selected_account = None
        self.COLORS = {
            "primary": "#3B82F6",
            "primary_hover": "#2563EB",
            "success": "#10B981",
            "success_hover": "#059669",
            "neutral": "#6B7280",
            "neutral_hover": "#4B5563",
            "background": "#1E293B",
            "card": "#2A2A3C",
            "text": "#E5E7EB",
            "accent": "#60A5FA",
            "error": "#EF4444",
            "highlight": "#93C5FD"
        }
        self.FONTS = {
            "title": ("Helvetica", 28, "bold"),
            "subtitle": ("Helvetica", 20),
            "label": ("Helvetica", 16),
            "button": ("Helvetica", 16, "bold"),
            "text": ("Helvetica", 14),
        }
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color=self.COLORS["background"])
        self.show_login_frame()

    def interpolate_color(self, start_color, end_color, t):
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        interpolated_rgb = tuple(int(start + (end - start) * t) for start, end in zip(start_rgb, end_rgb))
        return f"#{interpolated_rgb[0]:02x}{interpolated_rgb[1]:02x}{interpolated_rgb[2]:02x}"

    def clear_frame(self, fade_out=False):
        if self.current_frame:
            if fade_out:
                start_color = self.COLORS["card"]
                end_color = self.COLORS["background"]
                for i in range(10, -1, -1):
                    t = i / 10.0
                    color = self.interpolate_color(start_color, end_color, t)
                    self.current_frame.configure(fg_color=color)
                    self.current_frame.update()
                    self.current_frame.after(30)
            self.current_frame.destroy()

    def show_login_frame(self):
        self.clear_frame(fade_out=True)
        self.current_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["card"], corner_radius=15, border_width=2, border_color=self.COLORS["accent"])
        self.current_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        ctk.CTkLabel(
            self.current_frame,
            text="🏦 Елітна Банківська Система",
            font=self.FONTS["title"],
            text_color=self.COLORS["accent"]
        ).pack(pady=20)
        form_frame = ctk.CTkFrame(self.current_frame, fg_color=self.COLORS["card"], corner_radius=10)
        form_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(form_frame, text="👤 Ім'я користувача", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=(20, 5))
        username_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Введіть ім'я користувача",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        username_entry.pack(pady=5)
        username_entry.bind("<FocusIn>", lambda e: username_entry.configure(border_color=self.COLORS["highlight"]))
        username_entry.bind("<FocusOut>", lambda e: username_entry.configure(border_color=self.COLORS["accent"]))
        ctk.CTkLabel(form_frame, text="🔒 Пароль", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            show="*",
            placeholder_text="Введіть пароль",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        password_entry.pack(pady=5)
        password_entry.bind("<FocusIn>", lambda e: password_entry.configure(border_color=self.COLORS["highlight"]))
        password_entry.bind("<FocusOut>", lambda e: password_entry.configure(border_color=self.COLORS["accent"]))
        login_button = ctk.CTkButton(
            form_frame,
            text="🔑 Увійти",
            command=lambda: self.handle_login(username_entry.get(), password_entry.get()),
            font=self.FONTS["button"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        login_button.pack(pady=15)
        login_button.bind("<Enter>", lambda e: login_button.configure(width=310, height=44))
        login_button.bind("<Leave>", lambda e: login_button.configure(width=300, height=40))
        register_button = ctk.CTkButton(
            form_frame,
            text="📝 Зареєструватися",
            command=self.show_register_frame,
            font=self.FONTS["button"],
            fg_color=self.COLORS["success"],
            hover_color=self.COLORS["success_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        register_button.pack(pady=5)
        register_button.bind("<Enter>", lambda e: register_button.configure(width=310, height=44))
        register_button.bind("<Leave>", lambda e: register_button.configure(width=300, height=40))

    def show_register_frame(self):
        self.clear_frame(fade_out=True)
        self.current_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["card"], corner_radius=15, border_width=2, border_color=self.COLORS["accent"])
        self.current_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        ctk.CTkLabel(
            self.current_frame,
            text="📝 Створити обліковий запис",
            font=self.FONTS["title"],
            text_color=self.COLORS["accent"]
        ).pack(pady=20)
        form_frame = ctk.CTkFrame(self.current_frame, fg_color=self.COLORS["card"], corner_radius=10)
        form_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(form_frame, text="👤 Ім'я користувача", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=(20, 5))
        username_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Введіть ім'я користувача",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        username_entry.pack(pady=5)
        username_entry.bind("<FocusIn>", lambda e: username_entry.configure(border_color=self.COLORS["highlight"]))
        username_entry.bind("<FocusOut>", lambda e: username_entry.configure(border_color=self.COLORS["accent"]))
        ctk.CTkLabel(form_frame, text="🔒 Пароль", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            show="*",
            placeholder_text="Введіть пароль",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        password_entry.pack(pady=5)
        password_entry.bind("<FocusIn>", lambda e: password_entry.configure(border_color=self.COLORS["highlight"]))
        password_entry.bind("<FocusOut>", lambda e: password_entry.configure(border_color=self.COLORS["accent"]))
        ctk.CTkLabel(form_frame, text="🔒 Підтвердити пароль", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        confirm_password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            show="*",
            placeholder_text="Підтвердьте пароль",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        confirm_password_entry.pack(pady=5)
        confirm_password_entry.bind("<FocusIn>", lambda e: confirm_password_entry.configure(border_color=self.COLORS["highlight"]))
        confirm_password_entry.bind("<FocusOut>", lambda e: confirm_password_entry.configure(border_color=self.COLORS["accent"]))
        ctk.CTkLabel(form_frame, text="🎭 Роль", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        role_var = ctk.StringVar(value="client")
        ctk.CTkRadioButton(
            form_frame,
            text="Клієнт",
            variable=role_var,
            value="client",
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_color=self.COLORS["accent"]
        ).pack(pady=5)
        ctk.CTkRadioButton(
            form_frame,
            text="Співробітник",
            variable=role_var,
            value="employee",
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_color=self.COLORS["accent"]
        ).pack(pady=5)
        register_button = ctk.CTkButton(
            form_frame,
            text="📝 Зареєструватися",
            command=lambda: self.handle_register(
                username_entry.get(), password_entry.get(), confirm_password_entry.get(), role_var.get()
            ),
            font=self.FONTS["button"],
            fg_color=self.COLORS["success"],
            hover_color=self.COLORS["success_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        register_button.pack(pady=15)
        register_button.bind("<Enter>", lambda e: register_button.configure(width=310, height=44))
        register_button.bind("<Leave>", lambda e: register_button.configure(width=300, height=40))
        back_button = ctk.CTkButton(
            form_frame,
            text="⬅ Назад",
            command=self.show_login_frame,
            font=self.FONTS["button"],
            fg_color=self.COLORS["neutral"],
            hover_color=self.COLORS["neutral_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        back_button.pack(pady=5)
        back_button.bind("<Enter>", lambda e: back_button.configure(width=310, height=44))
        back_button.bind("<Leave>", lambda e: back_button.configure(width=300, height=40))

    def handle_register(self, username, password, confirm_password, role):
        error_label = ctk.CTkLabel(self.current_frame, text="", text_color=self.COLORS["error"], font=self.FONTS["text"])
        error_label.pack()
        if not username or not password or not confirm_password:
            error_label.configure(text="Усі поля обов'язкові")
            return
        if password != confirm_password:
            error_label.configure(text="Паролі не збігаються")
            return
        if len(password) < 6:
            error_label.configure(text="Пароль має містити щонайменше 6 символів")
            return
        if not all(c.isalpha() for c in username):
            error_label.configure(text="Ім'я користувача має містити лише літери")
            return
        success, message = self.db.register_user(username, password, UserRole(role))
        error_label.configure(text=message, text_color=self.COLORS["success"] if success else self.COLORS["error"])
        if success:
            self.db.log_action(f"Користувач зареєстрований: {username}")
            self.root.after(1000, self.show_login_frame)

    def handle_login(self, username, password):
        error_label = ctk.CTkLabel(self.current_frame, text="", text_color=self.COLORS["error"], font=self.FONTS["text"])
        error_label.pack()
        if self.auth.login(username, password):
            self.db.log_action(f"Користувач увійшов: {username}")
            if self.auth.current_user.role == UserRole.CLIENT:
                self.show_client_frame()
            else:
                self.show_employee_frame()
        else:
            error_label.configure(text="Невірне ім'я користувача або пароль")

    def show_client_frame(self):
        self.clear_frame(fade_out=True)
        self.current_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["card"], corner_radius=15, border_width=2, border_color=self.COLORS["accent"])
        self.current_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        accounts = self.db.get_user_accounts(self.auth.current_user.user_id)
        if not accounts:
            ctk.CTkLabel(self.current_frame, text="Рахунки не знайдені", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=20)
            return
        self.selected_account = accounts[0]
        ctk.CTkLabel(
            self.current_frame,
            text=f"👋 Вітаємо, {self.auth.current_user.username}",
            font=self.FONTS["title"],
            text_color=self.COLORS["accent"]
        ).pack(pady=10)
        account_entry = ctk.CTkEntry(
            self.current_frame,
            width=300,
            text_color=self.COLORS["text"],
            fg_color=self.COLORS["background"],
            border_color=self.COLORS["accent"],
            corner_radius=8,
            state="readonly"
        )
        account_entry.insert(0, self.selected_account.account_id)
        account_entry.pack(pady=5)
        account_var = ctk.StringVar(value=self.selected_account.account_id)
        account_menu = ctk.CTkOptionMenu(
            self.current_frame,
            values=[account.account_id for account in accounts],
            variable=account_var,
            command=lambda account_id: [self.update_selected_account(account_id, balance_label), account_entry.configure(state="normal"), account_entry.delete(0, "end"), account_entry.insert(0, account_id), account_entry.configure(state="readonly")],
            fg_color=self.COLORS["primary"],
            button_color=self.COLORS["primary"],
            button_hover_color=self.COLORS["primary_hover"],
            text_color=self.COLORS["text"],
            dropdown_fg_color=self.COLORS["card"],
            dropdown_text_color=self.COLORS["text"],
            dropdown_hover_color=self.COLORS["primary_hover"]
        )
        account_menu.pack(pady=5)
        balance_label = ctk.CTkLabel(
            self.current_frame,
            text=f"💰 Баланс: ${self.selected_account.balance:.2f}",
            font=self.FONTS["subtitle"],
            text_color=self.COLORS["text"]
        )
        balance_label.pack(pady=5)
        scrollable_frame = ctk.CTkScrollableFrame(self.current_frame, fg_color=self.COLORS["card"], corner_radius=10)
        scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)
        form_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.COLORS["card"], corner_radius=10)
        form_frame.pack(fill="x")
        ctk.CTkLabel(form_frame, text="💸 Сума депозиту", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=(10, 5))
        deposit_amount = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Введіть суму",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        deposit_amount.pack(pady=5)
        deposit_amount.bind("<FocusIn>", lambda e: deposit_amount.configure(border_color=self.COLORS["highlight"]))
        deposit_amount.bind("<FocusOut>", lambda e: deposit_amount.configure(border_color=self.COLORS["accent"]))
        deposit_button = ctk.CTkButton(
            form_frame,
            text="💰 Депозит",
            command=lambda: self.handle_deposit(self.selected_account, deposit_amount.get(), balance_label),
            font=self.FONTS["button"],
            fg_color=self.COLORS["success"],
            hover_color=self.COLORS["success_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        deposit_button.pack(pady=10)
        deposit_button.bind("<Enter>", lambda e: deposit_button.configure(width=310, height=44))
        deposit_button.bind("<Leave>", lambda e: deposit_button.configure(width=300, height=40))
        ctk.CTkLabel(form_frame, text="💸 Сума переказу", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        transfer_amount = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Введіть суму",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        transfer_amount.pack(pady=5)
        transfer_amount.bind("<FocusIn>", lambda e: transfer_amount.configure(border_color=self.COLORS["highlight"]))
        transfer_amount.bind("<FocusOut>", lambda e: transfer_amount.configure(border_color=self.COLORS["accent"]))
        ctk.CTkLabel(form_frame, text="👤 Ім'я отримувача", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        recipient_username = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Введіть ім'я користувача",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        recipient_username.pack(pady=5)
        recipient_username.bind("<FocusIn>", lambda e: recipient_username.configure(border_color=self.COLORS["highlight"]))
        recipient_username.bind("<FocusOut>", lambda e: recipient_username.configure(border_color=self.COLORS["accent"]))
        transfer_button = ctk.CTkButton(
            form_frame,
            text="💸 Переказ",
            command=lambda: self.handle_transfer(self.selected_account, transfer_amount.get(), recipient_username.get(), balance_label),
            font=self.FONTS["button"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        transfer_button.pack(pady=10)
        transfer_button.bind("<Enter>", lambda e: transfer_button.configure(width=310, height=44))
        transfer_button.bind("<Leave>", lambda e: transfer_button.configure(width=300, height=40))
        ctk.CTkLabel(form_frame, text="📄 Сума оплати рахунку", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        bill_amount = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Введіть суму",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        bill_amount.pack(pady=5)
        bill_amount.bind("<FocusIn>", lambda e: bill_amount.configure(border_color=self.COLORS["highlight"]))
        bill_amount.bind("<FocusOut>", lambda e: bill_amount.configure(border_color=self.COLORS["accent"]))
        bill_button = ctk.CTkButton(
            form_frame,
            text="📄 Оплатити рахунок",
            command=lambda: self.handle_bill_payment(self.selected_account, bill_amount.get(), balance_label),
            font=self.FONTS["button"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        bill_button.pack(pady=10)
        bill_button.bind("<Enter>", lambda e: bill_button.configure(width=310, height=44))
        bill_button.bind("<Leave>", lambda e: bill_button.configure(width=300, height=40))
        create_account_button = ctk.CTkButton(
            form_frame,
            text="➕ Створити новий рахунок",
            command=self.handle_create_account,
            font=self.FONTS["button"],
            fg_color=self.COLORS["success"],
            hover_color=self.COLORS["success_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        create_account_button.pack(pady=10)
        create_account_button.bind("<Enter>", lambda e: create_account_button.configure(width=310, height=44))
        create_account_button.bind("<Leave>", lambda e: create_account_button.configure(width=300, height=40))
        transactions_button = ctk.CTkButton(
            form_frame,
            text="📜 Переглянути транзакції",
            command=lambda: self.show_transactions(self.selected_account),
            font=self.FONTS["button"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        transactions_button.pack(pady=10)
        transactions_button.bind("<Enter>", lambda e: transactions_button.configure(width=310, height=44))
        transactions_button.bind("<Leave>", lambda e: transactions_button.configure(width=300, height=40))
        logout_button = ctk.CTkButton(
            form_frame,
            text="🚪 Вийти",
            command=lambda: [self.auth.logout(), self.show_login_frame()],
            font=self.FONTS["button"],
            fg_color=self.COLORS["success"],
            hover_color=self.COLORS["success_hover"],
            border_width=4,
            border_color=self.COLORS["highlight"],
            corner_radius=10,
            width=320,
            height=48
        )
        logout_button.pack(pady=30, side="bottom")
        logout_button.bind("<Enter>", lambda e: logout_button.configure(width=330, height=52))
        logout_button.bind("<Leave>", lambda e: logout_button.configure(width=320, height=48))

    def update_selected_account(self, account_id, balance_label):
        accounts = self.db.get_user_accounts(self.auth.current_user.user_id)
        for account in accounts:
            if account.account_id == account_id:
                self.selected_account = account
                balance_label.configure(text=f"💰 Баланс: ${self.selected_account.balance:.2f}")
                break

    def handle_deposit(self, account, amount_str, balance_label):
        error_label = ctk.CTkLabel(self.current_frame, text="", text_color=self.COLORS["error"],
                                   font=self.FONTS["text"])
        error_label.pack()
        try:
            amount = float(amount_str)
            if amount <= 0:
                error_label.configure(text="Невірна сума")
                return
            success, message = self.db.add_deposit(account, amount)
            if not success:
                error_label.configure(text=message)
                return
            self.db.log_action(f"Депозит: ${amount:.2f} на рахунок {account.account_id}")
            error_label.configure(text="Депозит успішний", text_color=self.COLORS["success"])
            balance_label.configure(text=f"💰 Баланс: ${account.balance:.2f}")
        except ValueError:
            error_label.configure(text="Невірне введення")

    def handle_transfer(self, account, amount_str, recipient_username, balance_label):
        error_label = ctk.CTkLabel(self.current_frame, text="", text_color=self.COLORS["error"], font=self.FONTS["text"])
        error_label.pack()
        try:
            amount = float(amount_str)
            if account.is_blocked:
                error_label.configure(text="Рахунок заблоковано")
                return
            if amount <= 0 or amount > account.balance:
                error_label.configure(text="Невірна сума")
                return
            if recipient_username == self.auth.current_user.username:
                error_label.configure(text="Неможливо переказати собі")
                return
            recipient_user = self.db.get_user_by_username(recipient_username)
            if not recipient_user:
                error_label.configure(text="Отримувача не знайдено")
                return
            recipient_accounts = self.db.get_user_accounts(recipient_user.user_id)
            if not recipient_accounts:
                error_label.configure(text="У отримувача немає активних рахунків")
                return
            recipient_account = recipient_accounts[0]  # Use first account of recipient
            if recipient_account.is_blocked:
                error_label.configure(text="Рахунок отримувача заблоковано")
                return
            account.balance -= amount
            recipient_account.balance += amount
            self.db.add_transaction(Transaction(generate_id(), account.account_id, -amount, "transfer"))
            self.db.add_transaction(Transaction(generate_id(), recipient_account.account_id, amount, "transfer"))
            self.db.log_action(f"Переказ: ${amount:.2f} з {account.account_id} на {recipient_account.account_id} (користувач: {recipient_username})")
            error_label.configure(text="Переказ успішний", text_color=self.COLORS["success"])
            balance_label.configure(text=f"💰 Баланс: ${account.balance:.2f}")
        except ValueError:
            error_label.configure(text="Невірне введення")

    def handle_bill_payment(self, account, amount_str, balance_label):
        error_label = ctk.CTkLabel(self.current_frame, text="", text_color=self.COLORS["error"], font=self.FONTS["text"])
        error_label.pack()
        try:
            amount = float(amount_str)
            if account.is_blocked:
                error_label.configure(text="Рахунок заблоковано")
                return
            if amount <= 0 or amount > account.balance:
                error_label.configure(text="Невірна сума")
                return
            account.balance -= amount
            self.db.add_transaction(Transaction(generate_id(), account.account_id, -amount, "bill_payment"))
            self.db.log_action(f"Оплата рахунку: ${amount:.2f} з {account.account_id}")
            error_label.configure(text="Рахунок оплачено успішно", text_color=self.COLORS["success"])
            balance_label.configure(text=f"💰 Баланс: ${account.balance:.2f}")
        except ValueError:
            error_label.configure(text="Невірне введення")

    def handle_create_account(self):
        account_id = generate_id()
        self.db.create_account(self.auth.current_user.user_id, account_id)
        self.db.log_action(f"Новий рахунок створено: {account_id} для користувача {self.auth.current_user.user_id}")
        self.show_client_frame()

    def show_transactions(self, account):
        self.clear_frame(fade_out=True)
        self.current_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["card"], corner_radius=15, border_width=2, border_color=self.COLORS["accent"])
        self.current_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        ctk.CTkLabel(
            self.current_frame,
            text="📜 Історія транзакцій",
            font=self.FONTS["title"],
            text_color=self.COLORS["accent"]
        ).pack(pady=10)
        sort_var = ctk.StringVar(value="date_desc")
        sort_menu = ctk.CTkOptionMenu(
            self.current_frame,
            values=["date_desc", "date_asc", "amount_desc", "amount_asc"],
            variable=sort_var,
            command=lambda x: self.update_transactions(account, sort_var.get(), scroll_frame),
            fg_color=self.COLORS["primary"],
            button_color=self.COLORS["primary"],
            button_hover_color=self.COLORS["primary_hover"],
            text_color=self.COLORS["text"],
            dropdown_fg_color=self.COLORS["card"],
            dropdown_text_color=self.COLORS["text"],
            dropdown_hover_color=self.COLORS["primary_hover"]
        )
        sort_menu.pack(pady=5)
        scroll_frame = ctk.CTkScrollableFrame(self.current_frame, fg_color=self.COLORS["card"], corner_radius=10)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.update_transactions(account, sort_var.get(), scroll_frame)
        back_button = ctk.CTkButton(
            self.current_frame,
            text="⬅ Назад",
            command=self.show_client_frame,
            font=self.FONTS["button"],
            fg_color=self.COLORS["neutral"],
            hover_color=self.COLORS["neutral_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        back_button.pack(pady=10)
        back_button.bind("<Enter>", lambda e: back_button.configure(width=310, height=44))
        back_button.bind("<Leave>", lambda e: back_button.configure(width=300, height=40))

    def update_transactions(self, account, sort_key, scroll_frame):
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        transactions = self.db.get_account_transactions(account.account_id)
        if sort_key == "date_desc":
            transactions.sort(key=lambda t: t.timestamp, reverse=True)
        elif sort_key == "date_asc":
            transactions.sort(key=lambda t: t.timestamp)
        elif sort_key == "amount_desc":
            transactions.sort(key=lambda t: t.amount, reverse=True)
        elif sort_key == "amount_asc":
            transactions.sort(key=lambda t: t.amount)
        for t in transactions:
            ctk.CTkLabel(
                scroll_frame,
                text=f"{t.timestamp}: {t.transaction_type} ${t.amount:.2f}",
                font=self.FONTS["text"],
                text_color=self.COLORS["text"]
            ).pack(pady=5, padx=10, anchor="w")

    def show_employee_frame(self):
        self.clear_frame(fade_out=True)
        self.current_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["card"], corner_radius=15, border_width=2, border_color=self.COLORS["accent"])
        self.current_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        ctk.CTkLabel(
            self.current_frame,
            text=f"🛠 Панель співробітника: {self.auth.current_user.username}",
            font=self.FONTS["title"],
            text_color=self.COLORS["accent"]
        ).pack(pady=10)
        form_frame = ctk.CTkFrame(self.current_frame, fg_color=self.COLORS["card"], corner_radius=10)
        form_frame.pack(pady=10, padx=20, fill="x")
        transactions_button = ctk.CTkButton(
            form_frame,
            text="📜 Усі транзакції",
            command=self.show_all_transactions,
            font=self.FONTS["button"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        transactions_button.pack(pady=10)
        transactions_button.bind("<Enter>", lambda e: transactions_button.configure(width=310, height=44))
        transactions_button.bind("<Leave>", lambda e: transactions_button.configure(width=300, height=40))
        ctk.CTkLabel(form_frame, text="👤 ID рахунку для блокування/розблокування", font=self.FONTS["label"], text_color=self.COLORS["text"]).pack(pady=5)
        account_id_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Введіть ID рахунку",
            fg_color=self.COLORS["background"],
            text_color=self.COLORS["text"],
            border_color=self.COLORS["accent"],
            corner_radius=8
        )
        account_id_entry.pack(pady=5)
        account_id_entry.bind("<FocusIn>", lambda e: account_id_entry.configure(border_color=self.COLORS["highlight"]))
        account_id_entry.bind("<FocusOut>", lambda e: account_id_entry.configure(border_color=self.COLORS["accent"]))
        block_button = ctk.CTkButton(
            form_frame,
            text="🔒 Заблокувати рахунок",
            command=lambda: self.handle_block_account(account_id_entry.get()),
            font=self.FONTS["button"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        block_button.pack(pady=5)
        block_button.bind("<Enter>", lambda e: block_button.configure(width=310, height=44))
        block_button.bind("<Leave>", lambda e: block_button.configure(width=300, height=40))
        unblock_button = ctk.CTkButton(
            form_frame,
            text="🔓 Розблокувати рахунок",
            command=lambda: self.handle_unblock_account(account_id_entry.get()),
            font=self.FONTS["button"],
            fg_color=self.COLORS["primary"],
            hover_color=self.COLORS["primary_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        unblock_button.pack(pady=5)
        unblock_button.bind("<Enter>", lambda e: unblock_button.configure(width=310, height=44))
        unblock_button.bind("<Leave>", lambda e: unblock_button.configure(width=300, height=40))
        report_button = ctk.CTkButton(
            form_frame,
            text="📊 Згенерувати та експортувати звіт",
            command=self.generate_report,
            font=self.FONTS["button"],
            fg_color=self.COLORS["success"],
            hover_color=self.COLORS["success_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        report_button.pack(pady=10)
        report_button.bind("<Enter>", lambda e: report_button.configure(width=310, height=44))
        report_button.bind("<Leave>", lambda e: report_button.configure(width=300, height=40))
        logout_button = ctk.CTkButton(
            form_frame,
            text="🚪 Вийти",
            command=lambda: [self.auth.logout(), self.show_login_frame()],
            font=self.FONTS["button"],
            fg_color=self.COLORS["neutral"],
            hover_color=self.COLORS["neutral_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        logout_button.pack(pady=10)
        logout_button.bind("<Enter>", lambda e: logout_button.configure(width=310, height=44))
        logout_button.bind("<Leave>", lambda e: logout_button.configure(width=300, height=40))

    def show_all_transactions(self):
        self.clear_frame(fade_out=True)
        self.current_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["card"], corner_radius=15, border_width=2, border_color=self.COLORS["accent"])
        self.current_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        ctk.CTkLabel(
            self.current_frame,
            text="📜 Усі транзакції",
            font=self.FONTS["title"],
            text_color=self.COLORS["accent"]
        ).pack(pady=10)
        sort_var = ctk.StringVar(value="date_desc")
        sort_menu = ctk.CTkOptionMenu(
            self.current_frame,
            values=["date_desc", "date_asc", "amount_desc", "amount_asc"],
            variable=sort_var,
            command=lambda x: self.update_all_transactions(sort_var.get(), scroll_frame),
            fg_color=self.COLORS["primary"],
            button_color=self.COLORS["primary"],
            button_hover_color=self.COLORS["primary_hover"],
            text_color=self.COLORS["text"],
            dropdown_fg_color=self.COLORS["card"],
            dropdown_text_color=self.COLORS["text"],
            dropdown_hover_color=self.COLORS["primary_hover"]
        )
        sort_menu.pack(pady=5)
        scroll_frame = ctk.CTkScrollableFrame(self.current_frame, fg_color=self.COLORS["card"], corner_radius=10)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.update_all_transactions(sort_var.get(), scroll_frame)
        back_button = ctk.CTkButton(
            self.current_frame,
            text="⬅ Назад",
            command=self.show_employee_frame,
            font=self.FONTS["button"],
            fg_color=self.COLORS["neutral"],
            hover_color=self.COLORS["neutral_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        back_button.pack(pady=10)
        back_button.bind("<Enter>", lambda e: back_button.configure(width=310, height=44))
        back_button.bind("<Leave>", lambda e: back_button.configure(width=300, height=40))

    def update_all_transactions(self, sort_key, scroll_frame):
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        transactions = self.db.get_all_transactions()
        if sort_key == "date_desc":
            transactions.sort(key=lambda t: t.timestamp, reverse=True)
        elif sort_key == "date_asc":
            transactions.sort(key=lambda t: t.timestamp)
        elif sort_key == "amount_desc":
            transactions.sort(key=lambda t: t.amount, reverse=True)
        elif sort_key == "amount_asc":
            transactions.sort(key=lambda t: t.amount)
        for t in transactions:
            ctk.CTkLabel(
                scroll_frame,
                text=f"Рахунок {t.account_id}: {t.transaction_type} ${t.amount:.2f} о {t.timestamp}",
                font=self.FONTS["text"],
                text_color=self.COLORS["text"]
            ).pack(pady=5, padx=10, anchor="w")

    def handle_block_account(self, account_id):
        error_label = ctk.CTkLabel(self.current_frame, text="", text_color=self.COLORS["error"], font=self.FONTS["text"])
        error_label.pack()
        self.db.block_account(account_id)
        self.db.log_action(f"Рахунок заблоковано: {account_id}")
        error_label.configure(text=f"Рахунок {account_id} заблоковано", text_color=self.COLORS["success"])

    def handle_unblock_account(self, account_id):
        error_label = ctk.CTkLabel(self.current_frame, text="", text_color=self.COLORS["error"], font=self.FONTS["text"])
        error_label.pack()
        self.db.unblock_account(account_id)
        self.db.log_action(f"Рахунок розблоковано: {account_id}")
        error_label.configure(text=f"Рахунок {account_id} розблоковано", text_color=self.COLORS["success"])

    def generate_report(self):
        self.clear_frame(fade_out=True)
        self.current_frame = ctk.CTkFrame(self.root, fg_color=self.COLORS["card"], corner_radius=15, border_width=2, border_color=self.COLORS["accent"])
        self.current_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        ctk.CTkLabel(
            self.current_frame,
            text="📊 Звіт про транзакції",
            font=self.FONTS["title"],
            text_color=self.COLORS["accent"]
        ).pack(pady=10)
        transactions = self.db.get_all_transactions()
        total_deposits = sum(t.amount for t in transactions if t.transaction_type == "deposit")
        total_transfers = sum(t.amount for t in transactions if t.transaction_type == "transfer" and t.amount > 0)
        total_payments = sum(t.amount for t in transactions if t.transaction_type == "bill_payment")
        report_frame = ctk.CTkFrame(self.current_frame, fg_color=self.COLORS["card"], corner_radius=10)
        report_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(
            report_frame,
            text=f"💰 Загальні депозити: ${total_deposits:.2f}",
            font=self.FONTS["label"],
            text_color=self.COLORS["text"]
        ).pack(pady=5)
        ctk.CTkLabel(
            report_frame,
            text=f"💸 Загальні перекази: ${total_transfers:.2f}",
            font=self.FONTS["label"],
            text_color=self.COLORS["text"]
        ).pack(pady=5)
        ctk.CTkLabel(
            report_frame,
            text=f"📄 Загальні оплати рахунків: ${-total_payments:.2f}",
            font=self.FONTS["label"],
            text_color=self.COLORS["text"]
        ).pack(pady=5)
        self.db.export_report(total_deposits, total_transfers, -total_payments)
        self.db.log_action("Звіт експортовано")
        ctk.CTkLabel(
            self.current_frame,
            text="✅ Звіт експортовано до report.txt",
            font=self.FONTS["text"],
            text_color=self.COLORS["success"]
        ).pack(pady=5)
        back_button = ctk.CTkButton(
            self.current_frame,
            text="⬅ Назад",
            command=self.show_employee_frame,
            font=self.FONTS["button"],
            fg_color=self.COLORS["neutral"],
            hover_color=self.COLORS["neutral_hover"],
            border_width=2,
            border_color=self.COLORS["accent"],
            corner_radius=10,
            width=300,
            height=40
        )
        back_button.pack(pady=10)
        back_button.bind("<Enter>", lambda e: back_button.configure(width=310, height=44))
        back_button.bind("<Leave>", lambda e: back_button.configure(width=300, height=40))