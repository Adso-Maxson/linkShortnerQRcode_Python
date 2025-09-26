import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyshorteners
import qrcode
import os
from PIL import Image, ImageTk
import threading
import random
import time
import requests
from urllib.parse import urlparse

class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encurtador de URL com QR Code")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Serviços disponíveis com informações de confiabilidade
        self.services = {
            "TinyURL": {"method": "tinyurl", "reliable": True},
            "Is.gd": {"method": "isgd", "reliable": True},
            "Da.gd": {"method": "dagd", "reliable": True},
            "Chilp.it": {"method": "chilpit", "reliable": True},
            "Clck.ru": {"method": "clckru", "reliable": True},
            "Qps.ru": {"method": "qpsru", "reliable": True},
            "Ouo.io": {"method": "ouo", "reliable": True},
            "Git.io": {"method": "gitio", "reliable": False},  # Só GitHub
            "0x0.st": {"method": "nullpointer", "reliable": True},
            "Short.io": {"method": "shortio", "reliable": False},  # Precisa API
        }
        
        self.setup_style()
        self.create_widgets()
        
    def setup_style(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('TCombobox', font=('Arial', 10))
        
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Encurtador de URL + QR Code", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Frame de entrada da URL
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(url_frame, text="URL Original:").pack(anchor=tk.W)
        self.url_entry = ttk.Entry(url_frame, width=60, font=('Arial', 10))
        self.url_entry.pack(fill=tk.X, pady=5)
        self.url_entry.insert(0, "https://www.google.com")
        
        # Frame de seleção do serviço
        service_frame = ttk.Frame(main_frame)
        service_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(service_frame, text="Serviço de Encurtamento:").pack(anchor=tk.W)
        
        service_subframe = ttk.Frame(service_frame)
        service_subframe.pack(fill=tk.X, pady=5)
        
        self.service_var = tk.StringVar(value="TinyURL")
        service_names = list(self.services.keys())
        self.service_combo = ttk.Combobox(service_subframe, textvariable=self.service_var, 
                                         values=service_names, state="readonly", width=20)
        self.service_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.auto_service_var = tk.BooleanVar(value=True)
        self.auto_service_cb = ttk.Checkbutton(service_subframe, text="Tentar serviços automaticamente", 
                                              variable=self.auto_service_var,
                                              command=self.toggle_auto_mode)
        self.auto_service_cb.pack(side=tk.LEFT)
        
        # Frame de status dos serviços
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.status_text = tk.Text(self.status_frame, height=4, width=60, font=('Arial', 8))
        self.status_scrollbar = ttk.Scrollbar(self.status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=self.status_scrollbar.set)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(state=tk.DISABLED)
        
        # Frame dos botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.shorten_btn = ttk.Button(button_frame, text="Encurtar URL", command=self.shorten_url)
        self.shorten_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.generate_qr_btn = ttk.Button(button_frame, text="Gerar QR Code", command=self.generate_qr, state=tk.DISABLED)
        self.generate_qr_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(button_frame, text="Salvar QR Code", command=self.save_qr, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT)
        
        # Frame de resultados
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # URL encurtada
        ttk.Label(result_frame, text="URL Encurtada:").pack(anchor=tk.W)
        
        url_result_frame = ttk.Frame(result_frame)
        url_result_frame.pack(fill=tk.X, pady=5)
        
        self.short_url_var = tk.StringVar()
        short_url_entry = ttk.Entry(url_result_frame, textvariable=self.short_url_var, 
                                   state='readonly', width=50, font=('Arial', 10))
        short_url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        copy_btn = ttk.Button(url_result_frame, text="Copiar", command=self.copy_url, width=10)
        copy_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Status do serviço usado
        self.service_used_var = tk.StringVar(value="Serviço: Nenhum")
        service_label = ttk.Label(result_frame, textvariable=self.service_used_var, font=('Arial', 9))
        service_label.pack(anchor=tk.W)
        
        # Preview do QR Code
        qr_preview_frame = ttk.Frame(result_frame)
        qr_preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(qr_preview_frame, text="Preview do QR Code:").pack(anchor=tk.W, pady=(10, 5))
        
        # Container do QR Code
        self.qr_container = ttk.Frame(qr_preview_frame, relief='solid', borderwidth=1)
        self.qr_container.pack(fill=tk.BOTH, expand=True)
        self.qr_container.config(height=400)
        self.qr_container.pack_propagate(True)
        
        # Frame interno para centralizar o QR Code
        self.qr_frame = ttk.Frame(self.qr_container)
        self.qr_frame.pack(expand=True, fill=tk.BOTH)
        
        self.qr_label = ttk.Label(self.qr_frame, text="QR Code será exibido aqui\n", 
                                 background='white', anchor=tk.CENTER, justify=tk.CENTER,
                                 font=('Arial', 10))
        self.qr_label.pack(expand=True, fill=tk.BOTH)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        
        # Variáveis de controle
        self.qr_image = None
        self.qr_img_tk = None
        self.short_url = ""
        self.current_service = ""
        
    def toggle_auto_mode(self):
        """Habilita/desabilita a seleção de serviço manual"""
        if self.auto_service_var.get():
            self.service_combo.config(state='disabled')
        else:
            self.service_combo.config(state='readonly')
            
    def add_status_message(self, message):
        """Adiciona mensagem ao status"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
        
    def clear_status(self):
        """Limpa as mensagens de status"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
    def test_service_connection(self, service_name):
        """Testa se o serviço está acessível"""
        try:
            test_urls = {
                "TinyURL": "http://tinyurl.com",
                "Is.gd": "http://is.gd",
                "Da.gd": "http://da.gd",
                "Chilp.it": "http://chilp.it",
                "Clck.ru": "http://clck.ru",
                "Qps.ru": "http://qps.ru",
                "Ouo.io": "http://ouo.io",
                "0x0.st": "http://0x0.st",
            }
            
            if service_name in test_urls:
                response = requests.get(test_urls[service_name], timeout=10)
                return response.status_code == 200
            return True
        except:
            return False
    
    def try_service(self, service_name, url_original):
        """Tenta encurtar a URL usando um serviço específico"""
        try:
            self.add_status_message(f"Tentando {service_name}...")
            
            shortener = pyshorteners.Shortener()
            service_method = self.services[service_name]["method"]
            
            # Adiciona timeout explícito
            if service_method == "tinyurl":
                result = shortener.tinyurl.short(url_original)
            elif service_method == "isgd":
                result = shortener.isgd.short(url_original)
            elif service_method == "dagd":
                result = shortener.dagd.short(url_original)
            elif service_method == "chilpit":
                result = shortener.chilpit.short(url_original)
            elif service_method == "clckru":
                result = shortener.clckru.short(url_original)
            elif service_method == "qpsru":
                result = shortener.qpsru.short(url_original)
            elif service_method == "ouo":
                result = shortener.ouo.short(url_original)
            elif service_method == "nullpointer":
                result = shortener.nullpointer.short(url_original)
            elif service_method == "gitio":
                if 'github.com' in url_original or 'github.io' in url_original:
                    result = shortener.gitio.short(url_original)
                else:
                    raise Exception("Git.io só funciona com URLs do GitHub")
            else:
                result = shortener.tinyurl.short(url_original)
            
            if result and result.startswith('http'):
                self.add_status_message(f"✓ {service_name} funcionou!")
                return result
            else:
                self.add_status_message(f"✗ {service_name} retornou resultado inválido")
                return None
                
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "blocked" in error_msg.lower():
                self.add_status_message(f"✗ {service_name} bloqueado pela rede")
            elif "timed out" in error_msg.lower():
                self.add_status_message(f"✗ {service_name} timeout")
            else:
                self.add_status_message(f"✗ {service_name} erro: {error_msg[:50]}...")
            return None
    
    def shorten_url_auto(self, url_original):
        """Tenta encurtar a URL usando vários serviços automaticamente"""
        self.clear_status()
        self.add_status_message("Iniciando teste de serviços...")
        
        # Separa serviços por confiabilidade
        reliable_services = [name for name, info in self.services.items() if info["reliable"]]
        other_services = [name for name, info in self.services.items() if not info["reliable"]]
        
        # Embaralha os serviços
        random.shuffle(reliable_services)
        random.shuffle(other_services)
        
        # Tenta primeiro os serviços confiáveis
        all_services = reliable_services + other_services
        
        for service_name in all_services:
            # Pula Git.io se não for URL do GitHub
            if service_name == "Git.io" and not ('github.com' in url_original or 'github.io' in url_original):
                self.add_status_message("⏭️ Git.io pulado (não é URL do GitHub)")
                continue
                
            # Testa conexão primeiro
            if not self.test_service_connection(service_name):
                self.add_status_message(f"⏭️ {service_name} inacessível")
                continue
                
            result = self.try_service(service_name, url_original)
            if result:
                return result, service_name
                
            # Pequena pausa entre tentativas
            time.sleep(0.5)
                
        return None, "Nenhum"
    
    def shorten_url_thread(self):
        """Thread para encurtar URL sem travar a interface"""
        try:
            url_original = self.url_entry.get().strip()
            if not url_original:
                self.root.after(0, lambda: messagebox.showerror("Erro", "Por favor, digite uma URL"))
                return
                
            if not url_original.startswith(('http://', 'https://')):
                url_original = 'https://' + url_original
            
            if self.auto_service_var.get():
                # Modo automático: tenta vários serviços
                self.short_url, service_used = self.shorten_url_auto(url_original)
                self.current_service = service_used
            else:
                # Modo manual: usa o serviço selecionado
                selected_service = self.service_var.get()
                self.add_status_message(f"Tentando serviço manual: {selected_service}")
                self.short_url = self.try_service(selected_service, url_original)
                self.current_service = selected_service
            
            if self.short_url:
                self.root.after(0, self.update_short_url)
            else:
                self.root.after(0, lambda: messagebox.showerror("Erro", 
                    "Não foi possível encurtar a URL com nenhum serviço. Verifique sua conexão ou tente outro serviço manualmente."))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao encurtar URL: {str(e)}"))
        finally:
            self.root.after(0, self.hide_progress)
            
    def shorten_url(self):
        """Inicia o processo de encurtamento de URL"""
        self.show_progress()
        self.shorten_btn.config(state=tk.DISABLED)
        self.generate_qr_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.shorten_url_thread)
        thread.daemon = True
        thread.start()
        
    def update_short_url(self):
        """Atualiza a interface com a URL encurtada"""
        self.short_url_var.set(self.short_url)
        self.service_used_var.set(f"Serviço usado: {self.current_service}")
        self.generate_qr_btn.config(state=tk.NORMAL)
        self.add_status_message("✓ Processo concluído com sucesso!")
        
    def generate_qr(self):
        """Gera o QR code a partir da URL encurtada"""
        try:
            if not self.short_url:
                messagebox.showerror("Erro", "Por favor, encurte a URL primeiro")
                return
                
            # Gerar QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.short_url)
            qr.make(fit=True)
            
            self.qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Aumentar o tamanho do QR code para a área maior
            qr_image_resized = self.qr_image.resize((300, 300), Image.Resampling.LANCZOS)
            self.qr_img_tk = ImageTk.PhotoImage(qr_image_resized)
            
            # Atualizar preview
            self.qr_label.config(image=self.qr_img_tk, text="")
            self.save_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar QR code: {str(e)}")
            
    def save_qr(self):
        """Salva o QR code em um arquivo"""
        try:
            if not self.qr_image:
                messagebox.showerror("Erro", "Nenhum QR code para salvar")
                return
                
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Salvar QR Code como"
            )
            
            if file_path:
                # Salva em alta resolução
                self.qr_image.save(file_path, quality=95)
                messagebox.showinfo("Sucesso", f"QR code salvo em:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar QR code: {str(e)}")
            
    def copy_url(self):
        """Copia a URL encurtada para a área de transferência"""
        if self.short_url:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.short_url)
            messagebox.showinfo("Sucesso", "URL copiada para a área de transferência")
        else:
            messagebox.showerror("Erro", "Nenhuma URL para copiar")
            
    def show_progress(self):
        """Mostra a barra de progresso"""
        self.progress.start()
        
    def hide_progress(self):
        """Esconde a barra de progresso"""
        self.progress.stop()
        self.shorten_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()