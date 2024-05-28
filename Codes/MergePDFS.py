import os
from tkinter import Tk, filedialog, Button, Label
import PyPDF2

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()

    if folder_path:
        label.config(text="Carpeta seleccionada: " + folder_path)
        confirm_button.config(state="normal")
        update_folder_info()

def update_folder_info():
    images = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'png', 'jpeg', 'JPG', 'jfif'))]
    pdfs = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    num_images = len(images)
    num_pdfs = len(pdfs)
    folder_info_label.config(text=f"Número total de imágenes encontradas: {num_images}. Número total de PDFs encontrados: {num_pdfs}.")

def merge_pdfs():
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not pdf_files:
        label.config(text="No se encontraron archivos PDF en la carpeta seleccionada.")
        return

    merged_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

    if not merged_pdf:
        label.config(text="No se ha especificado nombre para el archivo PDF unido.")
        return

    try:
        merger = PyPDF2.PdfMerger()
        for pdf_file in pdf_files:
            pdf_file_path = os.path.join(folder_path, pdf_file)
            merger.append(pdf_file_path)
        merger.write(merged_pdf)
        merger.close()
        if os.path.exists(merged_pdf):
            label.config(text=f"PDFs unidos en: {merged_pdf}")
        else:
            label.config(text="Error al crear el archivo PDF unido.")
    except Exception as e:
        label.config(text=f"Error al unir los archivos PDF: {e}")

root = Tk()
root.title("Convertidor de imágenes a PDF")
root.geometry("400x200")
folder_path = None

select_button = Button(root, text="Seleccionar carpeta", command=select_folder)
select_button.pack(pady=10)

confirm_button = Button(root, text="Unir PDFs", command=merge_pdfs, state="disabled")
confirm_button.pack(pady=10)

label = Label(root, text="")
label.pack()

folder_info_label = Label(root, text="")
folder_info_label.pack()

root.mainloop()
