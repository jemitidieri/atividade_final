# 1. SITUAÇÃO PROBLEMA: CADASTRO DE CLIENTES EM UM COMÉRCIO DE
# VAREJO
# A EMPRESA "XYZ COMÉRCIO" TEM DIFICULDADES EM CONTROLAR O
#  CADASTRO DE SEUS CLIENTES. ATUALMENTE, O ARQUIVO COM OS DADOS
# DOS CLIENTES ESTÁ DESORGANIZADO, E A EQUIPE DE VENDAS TEM
# ENCONTRADO DIFICULDADES EM ENCONTRAR INFORMAÇÕES RÁPIDO. A
# EMPRESA PRECISA DE UM SISTEMA QUE PERMITA O CADASTRO DE NOVOS
#CLIENTES, A CONSULTA DE CLIENTES JÁ CADASTRADOS E A EDIÇÃO OU
# EXCLUSÃO DE DADOS.
# Solução proposta: Criar um sistema que permita o cadastro de novos clientes
# com informações como nome, e-mail, telefone e endereço. Além disso, o
# sistema permitirá a consulta, edição e exclusão dos dados dos clientes
# através de uma interface gráfica simples.

import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter

def conectar():
    return sqlite3.connect('banco.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS usuarios(
              
              nome TEXT,
              email TEXT,
              telefone TEXT,
              endereco TEXT
              
              )
             ''')
    
    conn.commit()
    conn.close()

def inserir_usuario():
    nome  =  nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    endereco = endereco_entry.get()

    if nome and email and telefone and endereco:
        conn =  conectar()
        c = conn.cursor()
        c.execute("INSERT INTO usuarios VALUES(?,?,?,?)", (nome,email,telefone,endereco))
        conn.commit()
        conn.close()   
        messagebox.showinfo('', 'DADOS INSERIDOS COM SUCESSO!') 
        consultar_usuario() 
    else:
        messagebox.showwarning('','INSIRA OS DADOS SOLICITADOS')

def consultar_usuario():
    for row in tree.get_children():
        tree.delete(row)
        
    conn =  conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuario = c.fetchall()
    for us in usuario:
        tree.insert("", "end",values = (us[0], us[1],us[2], us[3]))
    conn.close()    

def editar_usuario():
    selecao = tree.selection()
    if selecao:
        dado_edit = tree.item(selecao)['values'][0]
        novo_nome = nome_entry.get()
        novo_email = email_entry.get()
        novo_telefone = telefone_entry.get()
        novo_endereco = endereco_entry.get()

        if novo_nome and novo_email and  novo_telefone and novo_endereco:
            conn =  conectar()
            c = conn.cursor()
            c.execute("UPDATE usuarios SET  nome = ?, email = ? , telefone =?, endereco =?  WHERE nome = ? ", (novo_nome, novo_email, novo_telefone, novo_endereco , dado_edit))
            conn.commit()
            conn.close()   
            messagebox.showinfo('', 'DADOS ATUALIZADOS COM SUCESSO!')  
            consultar_usuario()
        else:
            messagebox.showwarning('','TODOS OS DADOS PRECISAM SER PREENCHIDOS ')

def excluir_usuario():
    selecao = tree.selection()
    if selecao:
        user_del = tree.item(selecao)['values'][0]
        conn =  conectar()
        c = conn.cursor()     
        c.execute("DELETE FROM usuarios WHERE nome = ?", (user_del,))
        conn.commit()
        conn.close()
        messagebox.showinfo('', 'DADO DELETADO COM SUCESSO')
        consultar_usuario()
    else:
        messagebox.showerror('', 'ERRO AO DELETAR O DADO')    



#interface grafica

janela =  customtkinter.CTk()
janela.configure(fg_color='gray')
janela.title('CADASTRO DE CLIENTES')
janela.geometry('700x630')
caminho = 'icone_cliente.ico'
janela.iconbitmap(caminho)

tk.Label(janela, text = 'FORMULÁRIO ', font=('arial', 15)).grid(row=0, column=0, pady=10, padx=10)


#Abas de cadastro

fr0 =  customtkinter.CTkFrame(janela )
fr0.grid(columnspan=3)

nome_label =  tk.Label(fr0, text='Nome', font=('arial', 15))
nome_label.grid(row=1, column=0, pady=10, padx=10)

nome_entry = tk.Entry(fr0, font=('arial', 15))
nome_entry.grid(row=1, column=1, pady=10, padx=10)

email_label =  tk.Label(fr0, text='E-mail', font=('arial', 15))
email_label.grid(row=2, column=0, pady=10, padx=10)

email_entry = tk.Entry(fr0, font=('arial', 15))
email_entry.grid(row=2, column=1, pady=10, padx=10)


telefone_label =  tk.Label(fr0, text='Telefone', font=('arial', 15))
telefone_label.grid(row=3, column=0, pady=10, padx=10)

telefone_entry = tk.Entry(fr0, font=('arial', 15))
telefone_entry.grid(row=3, column=1, pady=10, padx=10)

endereco_label =  tk.Label(fr0, text='Endereço', font=('arial', 15))
endereco_label.grid(row=4, column=0, pady=10, padx=10)

endereco_entry = tk.Entry(fr0, font=('arial', 15))
endereco_entry.grid(row=4, column=1, pady=10, padx=10)

#botões

fr =  customtkinter.CTkFrame(janela)
fr.grid( columnspan=2)


btn_salvar =  customtkinter.CTkButton(fr, text= 'SALVAR', font=('arial', 15), command=inserir_usuario, fg_color='purple')
btn_salvar.grid(row=5, column=0, padx=10, pady=10)

btn_atualizar =  customtkinter.CTkButton(fr, text= 'ATUALIZAR', font=('arial', 15), command=editar_usuario, fg_color='blue')
btn_atualizar.grid(row=5, column=2, padx=10, pady=10)

btn_excluir =  customtkinter.CTkButton(fr, text= 'EXCLUIR', font=('arial', 15), command=excluir_usuario, fg_color='red')
btn_excluir.grid(row=5, column=3, padx=10, pady=10)

fr2 = customtkinter.CTkFrame(janela)
fr2.grid( columnspan=2)

colunas = ('NOME', 'E-MAIL', 'TELEFONE', 'ENDEREÇO')
tree =  ttk.Treeview(fr2, columns=colunas, show='headings', height=40)
tree.grid(row=6, column=0,padx=5, sticky='nsew')


for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor= tk.CENTER)


criar_tabela()
consultar_usuario()

janela.mainloop()