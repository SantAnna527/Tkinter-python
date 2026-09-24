import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

ARQUIVO = "despesas.json"

dados = []


def carregar_dados():
    global dados

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)

        atualizar_tabela()
        atualizar_saldo()


def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def atualizar_tabela(lista=None):
    for item in tree.get_children():
        tree.delete(item)

    if lista is None:
        lista = dados

    for i, registro in enumerate(lista):
        tree.insert(
            "",
            "end",
            iid=i,
            values=(
                registro["descricao"],
                registro["categoria"],
                registro["data"],
                registro["tipo"],
                f"R$ {registro['valor']:.2f}"
            )
        )


def atualizar_saldo():
    saldo = 0

    for item in dados:
        if item["tipo"] == "Receita":
            saldo += item["valor"]
        else:
            saldo -= item["valor"]

    lbl_saldo.config(text=f"Saldo Atual: R$ {saldo:.2f}")


def limpar():
    entry_descricao.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_valor.delete(0, tk.END)

    tipo_var.set("Receita")


def cadastrar():
    descricao = entry_descricao.get().strip()
    categoria = entry_categoria.get().strip()
    data = entry_data.get().strip()
    tipo = tipo_var.get()

    try:
        valor = float(entry_valor.get())
    except:
        messagebox.showerror("Erro", "Valor inválido.")
        return

    if not descricao or not categoria or not data:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    if valor <= 0:
        messagebox.showwarning("Aviso", "Valor deve ser maior que zero.")
        return

    dados.append({
        "descricao": descricao,
        "categoria": categoria,
        "data": data,
        "tipo": tipo,
        "valor": valor
    })

    salvar_dados()
    atualizar_tabela()
    atualizar_saldo()
    limpar()

    messagebox.showinfo("Sucesso", "Registro cadastrado.")


def selecionar(event):
    selecionado = tree.focus()

    if not selecionado:
        return

    valores = tree.item(selecionado)["values"]

    entry_descricao.delete(0, tk.END)
    entry_descricao.insert(0, valores[0])

    entry_categoria.delete(0, tk.END)
    entry_categoria.insert(0, valores[1])

    entry_data.delete(0, tk.END)
    entry_data.insert(0, valores[2])

    tipo_var.set(valores[3])

    valor = str(valores[4]).replace("R$ ", "")
    entry_valor.delete(0, tk.END)
    entry_valor.insert(0, valor)


def editar():
    selecionado = tree.focus()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro.")
        return

    try:
        valor = float(entry_valor.get())
    except:
        messagebox.showerror("Erro", "Valor inválido.")
        return

    dados[int(selecionado)] = {
        "descricao": entry_descricao.get(),
        "categoria": entry_categoria.get(),
        "data": entry_data.get(),
        "tipo": tipo_var.get(),
        "valor": valor
    }

    salvar_dados()
    atualizar_tabela()
    atualizar_saldo()

    messagebox.showinfo("Sucesso", "Registro atualizado.")


def excluir():
    selecionado = tree.focus()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro.")
        return

    confirmar = messagebox.askyesno(
        "Confirmar",
        "Deseja realmente excluir?"
    )

    if confirmar:
        dados.pop(int(selecionado))

        salvar_dados()
        atualizar_tabela()
        atualizar_saldo()
        limpar()


def pesquisar():
    termo = entry_pesquisa.get().lower()

    resultado = []

    for item in dados:
        if termo in item["descricao"].lower():
            resultado.append(item)

    atualizar_tabela(resultado)




janela = tk.Tk()
janela.title("Controle Fácil")
janela.geometry("900x600")



tk.Label(janela, text="Descrição").pack()
entry_descricao = tk.Entry(janela, width=40)
entry_descricao.pack()

tk.Label(janela, text="Categoria").pack()
entry_categoria = tk.Entry(janela, width=40)
entry_categoria.pack()

tk.Label(janela, text="Data").pack()
entry_data = tk.Entry(janela, width=40)
entry_data.pack()

tk.Label(janela, text="Tipo").pack()

tipo_var = tk.StringVar(value="Receita")

ttk.Combobox(
    janela,
    textvariable=tipo_var,
    values=["Receita", "Despesa"],
    state="readonly"
).pack()

tk.Label(janela, text="Valor").pack()
entry_valor = tk.Entry(janela, width=40)
entry_valor.pack()



frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Cadastrar", command=cadastrar).grid(row=0, column=0)
tk.Button(frame_botoes, text="Editar", command=editar).grid(row=0, column=1)
tk.Button(frame_botoes, text="Excluir", command=excluir).grid(row=0, column=2)
tk.Button(frame_botoes, text="Limpar", command=limpar).grid(row=0, column=3)



tk.Label(janela, text="Pesquisar").pack()

entry_pesquisa = tk.Entry(janela, width=40)
entry_pesquisa.pack()

tk.Button(janela, text="Buscar", command=pesquisar).pack()



colunas = ("Descrição", "Categoria", "Data", "Tipo", "Valor")

tree = ttk.Treeview(
    janela,
    columns=colunas,
    show="headings",
    height=12
)

for col in colunas:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", selecionar)



lbl_saldo = tk.Label(
    janela,
    text="Saldo Atual: R$ 0.00",
    font=("Arial", 12, "bold")
)

lbl_saldo.pack(pady=10)

carregar_dados()

janela.mainloop()