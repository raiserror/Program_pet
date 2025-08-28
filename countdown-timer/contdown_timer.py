import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import pygame
import math
import sys

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False
    print("⚠️ winsound недоступен (не Windows система)")

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер обратного отсчета")
        self.root.geometry("500x720")
        self.root.minsize(450, 650)
        self.root.configure(bg='#2c3e50')
        
        self.center_window()
        
        # Инициализация pygame для звука
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except Exception as e:
            print(f"Ошибка инициализации звука: {e}")
            messagebox.showwarning("Внимание", "Звук недоступен. Проверьте аудиосистему.")
        
        # Переменные
        self.is_running = False
        self.remaining_time = 0
        self.total_seconds = 0
        self.last_signal_time = 0
        self.signal_check_id = None
        self.beep_sound = HAS_WINSOUND 
        
        # Стили
        self.setup_styles()
        self.setup_ui()
        self.load_sound()
        
        # Анимация
        self.animate_progress()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#2c3e50')
        style.configure('Dark.TLabel', background='#2c3e50', foreground='#ecf0f1', font=('Segoe UI', 10))
        style.configure('Title.TLabel', background='#2c3e50', foreground='#3498db', font=('Segoe UI', 18, 'bold'))
        style.configure('Time.TLabel', background='#34495e', foreground='#ecf0f1', font=('Consolas', 32, 'bold'))
        style.configure('Small.TLabel', background='#2c3e50', foreground='#bdc3c7', font=('Segoe UI', 9))
        style.configure('Primary.TButton', background='#3498db', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', background='#27ae60', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('Danger.TButton', background='#e74c3c', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.configure('Warning.TButton', background='#f39c12', foreground='white', font=('Segoe UI', 10, 'bold'))
    
    def setup_ui(self):
        main_container = ttk.Frame(self.root, style='Dark.TFrame', padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_container, style='Dark.TFrame')
        header_frame.pack(pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="⏰ Таймер обратного отсчета", style='Title.TLabel')
        title_label.pack()
        
        # Область ввода времени
        input_frame = ttk.Frame(main_container, style='Dark.TFrame')
        input_frame.pack(pady=15)
        
        time_inputs = [
            ("Часы", "hours", 0, 23),
            ("Минуты", "minutes", 0, 59),
            ("Секунды", "seconds", 0, 59)
        ]
        
        self.time_vars = {}
        for i, (label_text, name, from_, to) in enumerate(time_inputs):
            frame = ttk.Frame(input_frame, style='Dark.TFrame')
            frame.grid(row=0, column=i, padx=8)
            
            label = ttk.Label(frame, text=label_text, style='Dark.TLabel')
            label.pack()
            
            var = tk.StringVar(value="0" if name != "seconds" else "30")
            self.time_vars[name] = var
            
            spinbox = ttk.Spinbox(frame, from_=from_, to=to, width=8,
                                 textvariable=var, font=('Segoe UI', 11),
                                 justify='center')
            spinbox.pack(pady=4)
        
        # Настройка интервала сигналов
        signal_frame = ttk.Frame(main_container, style='Dark.TFrame')
        signal_frame.pack(pady=15)
        
        ttk.Label(signal_frame, text="🔔 Сигнал каждые:", style='Dark.TLabel').pack()
        
        signal_input_frame = ttk.Frame(signal_frame, style='Dark.TFrame')
        signal_input_frame.pack(pady=5)
        
        self.signal_interval_var = tk.StringVar(value="10")
        self.signal_unit_var = tk.StringVar(value="seconds")
        
        self.signal_spin = ttk.Spinbox(signal_input_frame, from_=1, to=3600, width=8,
                                      textvariable=self.signal_interval_var, 
                                      font=('Segoe UI', 11), justify='center')
        self.signal_spin.pack(side=tk.LEFT, padx=5)
        
        self.unit_combo = ttk.Combobox(signal_input_frame, width=8,
                                      textvariable=self.signal_unit_var,
                                      font=('Segoe UI', 11), state="readonly")
        self.unit_combo['values'] = ('seconds', 'minutes')
        self.unit_combo.pack(side=tk.LEFT, padx=5)
        self.unit_combo.set('seconds')
        
        ttk.Label(signal_input_frame, text="(0 = только в конце)", style='Small.TLabel').pack(side=tk.LEFT, padx=10)
        
        # Дисплей таймера
        display_frame = ttk.Frame(main_container, style='Dark.TFrame')
        display_frame.pack(pady=20)
        
        self.canvas = tk.Canvas(display_frame, width=200, height=200, 
                               bg='#34495e', highlightthickness=0)
        self.canvas.pack()
        
        self.time_display = ttk.Label(display_frame, text="00:00:00", 
                                     style='Time.TLabel', background='#34495e')
        self.time_display.pack(pady=10)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_container, style='Dark.TFrame')
        button_frame.pack(pady=15)
        
        self.start_button = ttk.Button(button_frame, text="▶ Старт", 
                                      command=self.start_timer, style='Success.TButton')
        self.pause_button = ttk.Button(button_frame, text="⏸ Пауза", 
                                      command=self.pause_timer, style='Warning.TButton', state=tk.DISABLED)
        self.reset_button = ttk.Button(button_frame, text="↺ Сброс", 
                                      command=self.reset_timer, style='Primary.TButton')
        self.stop_button = ttk.Button(button_frame, text="⏹ Стоп", 
                                     command=self.stop_timer, style='Danger.TButton', state=tk.DISABLED)
        
        buttons = [self.start_button, self.pause_button, self.reset_button, self.stop_button]
        for i, button in enumerate(buttons):
            button.grid(row=0, column=i, padx=4, pady=4)
        
        # Статус бар
        status_frame = ttk.Frame(main_container, style='Dark.TFrame')
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, 
                              style='Dark.TLabel', foreground='#bdc3c7')
        status_bar.pack()
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var,
                                           maximum=100, style='Dark.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=5)
    
    def get_signal_interval_seconds(self):
        try:
            interval = int(self.signal_interval_var.get())
            unit = self.signal_unit_var.get()
            
            if interval == 0:
                return 0
                
            if unit == "minutes":
                return interval * 60
            else:
                return interval
                
        except ValueError:
            return 10
    
    def draw_progress_circle(self, progress):
        self.canvas.delete("all")
        self.canvas.create_oval(10, 10, 190, 190, outline='#7f8c8d', width=3, fill='#2c3e50')
        
        if progress > 0:
            self.canvas.create_arc(10, 10, 190, 190, 
                                  start=90, 
                                  extent=-360 * progress,
                                  outline='#3498db', 
                                  width=5, 
                                  style=tk.ARC)
        
        self.canvas.create_oval(50, 50, 150, 150, outline='#34495e', width=2, fill='#34495e')
    
    def animate_progress(self):
        if self.is_running and self.total_seconds > 0:
            progress = 1 - (self.remaining_time / self.total_seconds)
            self.draw_progress_circle(progress)
            self.progress_var.set(progress * 100)
        
        self.root.after(100, self.animate_progress)
    
    def load_sound(self):
        """Используем системный beep"""
        try:
            self.beep_sound = True  # Просто флаг что звук доступен
        except:
            self.beep_sound = None
            print("⚠️ Звук недоступен")

    def play_sound(self, sound_type="normal"):
        """Воспроизведение приятных звуков через winsound"""
        if self.beep_sound and HAS_WINSOUND:
            try:
                if sound_type == "interval":
                    tones = [523, 659, 784]  # C5, E5, G5 (мажорное трезвучие)
                    for tone in tones:
                        winsound.Beep(tone, 150)
                        time.sleep(0.05)
                    self.status_var.set(f"🔔 Сигнал! Осталось: {self.remaining_time} сек")
                    
                else:
                    tones = [784, 698, 659, 587, 523, 494, 440, 392]  # G5 до G4 нисходящая гамма
                    for tone in tones:
                        winsound.Beep(tone, 200)
                        time.sleep(0.03)
                    self.status_var.set("🎉 Время вышло!")
                    
            except Exception as e:
                print(f"❌ Ошибка воспроизведения: {e}")
                self.flash_window()
        else:
            print("⚠️ Звук недоступен - визуальная индикация")
            self.flash_window()
    
    def flash_window(self):
        """Мигание окна если звука нет"""
        original_color = self.root.cget("bg")
        for _ in range(3):
            self.root.configure(bg="#3498db")
            self.root.update()
            time.sleep(0.2)
            self.root.configure(bg=original_color)
            self.root.update()
            time.sleep(0.2)
    
    def check_signal_interval(self):
        """Проверка интервалов сигналов"""
        if not self.is_running:
            return
            
        interval_seconds = self.get_signal_interval_seconds()
        
        # Режим "только в конце"
        if interval_seconds == 0:
            return
            
        # Проверяем интервал
        elapsed = self.total_seconds - self.remaining_time
        if elapsed >= self.last_signal_time + interval_seconds:
            self.last_signal_time = elapsed
            self.play_sound("interval")
        
        # Продолжаем проверять
        if self.is_running:
            self.signal_check_id = self.root.after(1000, self.check_signal_interval)
    
    def update_display(self):
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_display.config(text=time_str)
        
        if self.remaining_time <= 10 and self.remaining_time > 0:
            self.time_display.config(foreground='#e74c3c')
        elif self.remaining_time == 0:
            self.time_display.config(foreground='#27ae60')
        else:
            self.time_display.config(foreground='#3498db')
    
    def start_timer(self):
        """Запускает таймер"""
        if not self.is_running:
            try:
                hours = int(self.time_vars['hours'].get())
                minutes = int(self.time_vars['minutes'].get())
                seconds = int(self.time_vars['seconds'].get())
                
                self.total_seconds = hours * 3600 + minutes * 60 + seconds
                
                if self.total_seconds <= 0:
                    messagebox.showwarning("Внимание", "Установите положительное время!")
                    return
                
                self.remaining_time = self.total_seconds
                self.is_running = True
                self.last_signal_time = 0
                
                self.update_buttons_state()
                self.status_var.set("⏰ Таймер запущен")
                self.draw_progress_circle(0)
                
                # Запускаем проверку сигналов
                self.check_signal_interval()
                
                # Запускаем основной таймер
                self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
                self.timer_thread.start()
                
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные числа!")
    
    def run_timer(self):
        """Основной цикл таймера"""
        while self.remaining_time > 0 and self.is_running:
            time.sleep(1)
            if self.is_running:
                self.remaining_time -= 1
                self.root.after(0, self.update_display)
        
        if self.remaining_time == 0 and self.is_running:
            self.root.after(0, self.timer_finished)
    
    def pause_timer(self):
        """Приостанавливает таймер"""
        self.is_running = not self.is_running
        if self.is_running:
            self.pause_button.config(text="⏸ Пауза")
            self.status_var.set("▶ Таймер продолжен")
            self.check_signal_interval()
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
        else:
            self.pause_button.config(text="▶ Продолжить")
            self.status_var.set("⏸ Таймер на паузе")
            if self.signal_check_id:
                self.root.after_cancel(self.signal_check_id)
    
    def reset_timer(self):
        """Сбрасывает таймер"""
        self.stop_timer()
        self.remaining_time = self.total_seconds
        self.update_display()
        self.draw_progress_circle(0)
        self.status_var.set("↺ Таймер сброшен")
    
    def stop_timer(self):
        """Полностью останавливает таймер"""
        self.is_running = False
        if self.signal_check_id:
            self.root.after_cancel(self.signal_check_id)
        self.update_buttons_state()
        self.status_var.set("⏹ Таймер остановлен")
    
    def timer_finished(self):
        """Действия по завершении таймера"""
        self.is_running = False
        if self.signal_check_id:
            self.root.after_cancel(self.signal_check_id)
        
        self.play_sound("end")
        self.update_buttons_state()
        self.status_var.set("🎉 Время вышло!")
        self.draw_progress_circle(1.0)
        
        messagebox.showinfo("Готово!", "⏰ Время вышло!\n\nТаймер завершил обратный отсчет.")
    
    def update_buttons_state(self):
        """Обновляет состояние кнопок"""
        if self.is_running:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL if self.total_seconds > 0 else tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()