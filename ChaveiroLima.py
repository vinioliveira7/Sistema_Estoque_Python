import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter.constants as tkc
import sqlite3
from datetime import datetime
from pytz import timezone

DEFAULT_FONT = "Arial 12"
DEFAULT_DATABASE = "banco_dados.db"
CHAVEIRO_ICON = "chaveiro_lima_icon.ico"
WARNING_MESSAGE = "Atenção!"

conn = sqlite3.connect(DEFAULT_DATABASE)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS estoque (
            id_chave INTEGER PRIMARY KEY,
            num_chave INTEGER,
            nom_chave TEXT,
            quant_chave INTEGER,
            val_chave REAL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT,
            senha TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY,
            data TEXT,
            cliente TEXT,
            produto TEXT,
            quantidade INTEGER,
            valor REAL)""")

conn.commit()

window = tk.Tk()
window.title("Chaveiro Lima")
window.geometry("400x400")
window["bg"] = "#EE8507"
window.resizable(0, 0)
icon_window = ImageTk.PhotoImage(file=CHAVEIRO_ICON)
window.iconbitmap(default=CHAVEIRO_ICON)
window.iconphoto(False, icon_window)
# Fundo
image = Image.open("window chaveiro.png")
photo = ImageTk.PhotoImage(image)
imagem = tk.Label(window, width=400, height=400, text="adicionando", image=photo)
imagem.image = photo
imagem.pack()

usuario = tk.StringVar()
senha = tk.StringVar()

style = ttk.Style()


def new_window():
    new_window = tk.Tk()
    new_window.geometry("400x400")
    new_window["bg"] = "#EE8507"
    new_window.resizable(0, 0)
    new_window.title("Tela de controle")
    icon_window = ImageTk.PhotoImage(file=CHAVEIRO_ICON)
    new_window.iconbitmap(default=CHAVEIRO_ICON)
    new_window.iconphoto(False, icon_window)

    # Tela 2
    image_nova = Image.open("tela_entretenimento.png")
    photo_nova = ImageTk.PhotoImage(image_nova)
    imagem_nova = tk.Label(
        new_window, width=400, height=400, text="adicionando2", image=photo_nova
    )
    imagem_nova.image = photo_nova
    imagem_nova.pack()

    clock_frame = tk.LabelFrame(
        new_window, width=370, height=200, bg="#EB622C", relief="flat"
    )
    clock_frame.place(x=250, y=280)

    label_clock = tk.Label(
        clock_frame, font=("Helvetica", 20), bg="#EB622C", fg="black", relief="flat"
    )
    label_clock.pack()
    clock(label_clock)

    # Botões new_window

    estoque = tk.Button(
        new_window,
        text="Estoque",
        width=11,
        font="normal 15",
        bd=3,
        relief="raised",
        highlightbackground="#EE8507",
        bg="#E57D27",
        fg="#636363",
        command=tela_estoque_func,
    ).place(y=20, x=15)

    clientes = tk.Button(
        new_window,
        text="Clientes",
        width=11,
        font="normal 15",
        bd=3,
        relief="raised",
        highlightbackground="#EE8507",
        bg="#E57D27",
        fg="#636363",
        command=tela_cliente_func,
    ).place(y=20, x=210)

    new_window.mainloop()


def analisar():
    select_senha = cur.execute(
        "SELECT senha FROM usuarios WHERE usuario=?", (usuario.get(),)
    )

    user_senha = select_senha.fetchone()
    senha_digitada = senha.get()
    if user_senha is None:
        messagebox.showwarning(
            title=WARNING_MESSAGE, message="Usuário ou Senha estão incorretos!"
        )
        return

    if user_senha[0] == senha_digitada:
        window.destroy()
        new_window()
    else:
        messagebox.showwarning(
            title=WARNING_MESSAGE, message="Usuário ou Senha estão incorretos!"
        )


def tela_cliente_func():
    conn = sqlite3.connect(DEFAULT_DATABASE)
    tela_cliente = tk.Toplevel()
    tela_cliente.geometry("800x600")
    tela_cliente.resizable(0, 0)
    tela_cliente.title("Tela de clientes")
    icon_window = ImageTk.PhotoImage(file=CHAVEIRO_ICON)
    tela_cliente.iconbitmap(default=CHAVEIRO_ICON)
    tela_cliente.iconphoto(False, icon_window)

    # Imagem tela cliente
    image_cliente = Image.open("tela_cliente.png")
    photo_cliente = ImageTk.PhotoImage(image_cliente)
    imagem_cliente = tk.Label(tela_cliente, width=800, height=600, image=photo_cliente)
    imagem_cliente.image = photo_cliente
    imagem_cliente.pack()

    cur = conn.cursor()
    produto_select = cur.execute("SELECT nom_chave FROM estoque")
    produto_fetch = produto_select.fetchall()
    print(produto_fetch)

    # Entry, Spinboxes tela cliente

    data_cliente = tk.StringVar()
    cliente_cliente = tk.StringVar()
    produto_cliente = tk.StringVar()
    quantidade_cliente = tk.IntVar()
    valor_cliente = tk.DoubleVar()

    id_cliente_retorno = cur.execute("SELECT id_cliente FROM clientes")
    retorno_ultimo_id_cliente = id_cliente_retorno.fetchall()[-1]
    print(retorno_ultimo_id_cliente[0])

    data_cliente_ent = tk.Entry(
        imagem_cliente,
        width=9,
        bd=2,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=data_cliente,
        justify="center",
    )
    data_cliente_ent.place(x=35, y=75)

    cliente_cliente_ent = tk.Entry(
        imagem_cliente,
        width=10,
        bd=2,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=cliente_cliente,
        justify="center",
    )
    cliente_cliente_ent.place(x=160, y=75)

    style.configure(
        "TCombobox",
        background="#3E362D",
        fieldbackground="#3E362D",
        font=("Latha", 20),
        foreground="#EEE3D5",
        borderwidth=2,
    )
    produto_combobox = ttk.Combobox(
        imagem_cliente,
        width=11,
        font="Verdana 12 bold",
        textvariable=produto_cliente,
        values=produto_fetch,
    )
    produto_combobox.place(x=300, y=75)

    quantidade_cliente_ent = tk.Entry(
        imagem_cliente,
        width=10,
        bd=2,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=quantidade_cliente,
        justify="center",
    )
    quantidade_cliente_ent.place(x=460, y=75)
    quantidade_cliente_ent.delete(0, tkc.END)

    valor_cliente_ent = tk.Entry(
        imagem_cliente,
        width=12,
        bd=2,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=valor_cliente,
        justify="center",
    )
    valor_cliente_ent.place(x=610, y=75)
    valor_cliente_ent.delete(0, tkc.END)

    lista_cliente_frame = tk.Frame(imagem_cliente, width=750, height=400)
    lista_cliente_frame.place(x=50, y=155)

    scroll_y_cliente = tk.Scrollbar(lista_cliente_frame, orient=tkc.VERTICAL)

    def cadastrar_cliente():
        conn = sqlite3.connect(DEFAULT_DATABASE)
        cur = conn.cursor()
        retorno_id_cliente = cur.fetchone()
        retorno_ultimo_id_cliente_soma = retorno_ultimo_id_cliente[0]
        retorno_ultimo_id_cliente_soma += 1
        print(retorno_ultimo_id_cliente_soma)

        produto_cliente_get = produto_cliente.get()

        print(produto_cliente.get())
        print("type produto", (type(produto_cliente.get())))
        print("get produto_cliente:", produto_cliente.get())
        cur.execute("SELECT nom_chave FROM estoque")
        fetch_produto = cur.fetchall()
        print(fetch_produto[0])

        for produto_cliente_for in fetch_produto:
            if produto_cliente_get in produto_cliente_for:
                print("tem no estoque")
                quant_estoque_sub_select = cur.execute(
                    "SELECT quant_chave FROM estoque WHERE nom_chave=?",
                    (produto_cliente.get(),),
                )
                quant_cliente_sub = quantidade_cliente.get()

                quant_estoque_sub_num = quant_estoque_sub_select.fetchone()[0]

                print("Quantidade no estoque:", quant_estoque_sub_num)
                print("Quantidade inserida:", quant_cliente_sub)

                resultado_estoque_sub = quant_estoque_sub_num - quant_cliente_sub
                print(resultado_estoque_sub)

                cur.execute(
                    """UPDATE estoque SET
                                quant_chave=:quant_chave_sub 
                                WHERE quant_chave=:quant_chave_antigo""",
                    {
                        "quant_chave_sub": resultado_estoque_sub,
                        "quant_chave_antigo": quant_estoque_sub_num,
                    },
                )

                if resultado_estoque_sub < 0:
                    messagebox.showwarning(
                        title="Sem estoque!",
                        message="O produto inserido não tem quantidade de estoque equivalente ao pedido!.",
                    )
                    return

        (
            cur.execute(
                "INSERT INTO clientes VALUES(?,?,?,?,?,?)",
                (
                    retorno_id_cliente,
                    data_cliente.get(),
                    cliente_cliente.get(),
                    produto_cliente.get(),
                    quantidade_cliente.get(),
                    valor_cliente.get(),
                ),
            ),
        )
        select_cliente = cur.execute("SELECT * FROM clientes")
        lista_cliente.insert(
            "",
            tkc.END,
            values=(
                retorno_ultimo_id_cliente_soma,
                data_cliente.get(),
                cliente_cliente.get(),
                produto_cliente.get(),
                quantidade_cliente.get(),
                valor_cliente.get(),
            ),
        )

        conn.commit()
        conn.close()

    lista_cliente = ttk.Treeview(
        lista_cliente_frame,
        height=18,
        columns=["id_cliente", "data", "cliente", "produto", "quantidade", "valor"],
        show="headings",
        yscrollcommand=scroll_y_cliente.set,
    )

    lista_cliente["displaycolumns"] = (
        "data",
        "cliente",
        "produto",
        "quantidade",
        "valor",
    )

    scroll_y_cliente.pack(side=tkc.LEFT, fill=tkc.Y)

    lista_cliente.heading("id_cliente", text="Id")
    lista_cliente.heading("data", text="Data")
    lista_cliente.heading("cliente", text="Cliente")
    lista_cliente.heading("produto", text="Produto")
    lista_cliente.heading("quantidade", text="Quantidade")
    lista_cliente.heading("valor", text="Valor")

    lista_cliente.column("id_cliente", width=100, anchor=tkc.CENTER)
    lista_cliente.column("data", width=100, anchor=tkc.CENTER)
    lista_cliente.column("cliente", width=100)
    lista_cliente.column("quantidade", width=100, anchor=tkc.CENTER)
    lista_cliente.column("valor", width=100, anchor=tkc.CENTER)

    lista_cliente.pack(fill=tkc.BOTH, expand=tkc.TRUE)

    lista_cliente.bind(
        "<ButtonRelease-1>",
        lambda eff: selecionar_item_cliente(
            eff,
            lista_cliente,
            data_cliente_ent,
            cliente_cliente_ent,
            produto_combobox,
            quantidade_cliente_ent,
            valor_cliente_ent,
        ),
    )

    cur.execute("SELECT * FROM clientes ORDER BY id_cliente")
    select_cliente_ins = cur.fetchall()
    for item_cliente in select_cliente_ins:
        lista_cliente.insert(
            "",
            tkc.END,
            iid=item_cliente[0],
            values=(
                item_cliente[0],
                item_cliente[1],
                item_cliente[2],
                item_cliente[3],
                item_cliente[4],
                item_cliente[5],
            ),
        )
        conn.commit()

    enviar_cadastro_cliente = tk.Button(
        imagem_cliente,
        width=6,
        height=1,
        text="Enviar",
        bd=3,
        relief="ridge",
        bg="#2DB00D",
        highlightbackground="#32FF00",
        activebackground="#80C270",
        command=cadastrar_cliente,
    ).place(x=675, y=150)

    update_cadastro_cliente = tk.Button(
        imagem_cliente,
        width=6,
        height=1,
        text="Atualizar",
        bd=3,
        relief="ridge",
        bg="#FFFB07",
        highlightbackground="#F7FF00",
        activebackground="#FFD100",
        command=lambda: atualizar_cliente(
            lista_cliente,
            data_cliente,
            cliente_cliente,
            produto_cliente,
            quantidade_cliente,
            valor_cliente,
        ),
    ).place(x=675, y=190)

    delete_cadastro_cliente = tk.Button(
        imagem_cliente,
        width=6,
        height=1,
        text="Deletar",
        bd=3,
        relief="ridge",
        bg="#BE1A07",
        highlightbackground="#BE1A07",
        activebackground="#E57365",
        command=lambda: deletar_cliente(
            lista_cliente,
            data_cliente_ent,
            cliente_cliente_ent,
            produto_combobox,
            quantidade_cliente_ent,
            valor_cliente_ent,
        ),
    ).place(x=675, y=230)

    tela_cliente.mainloop()


# Funções da tela entretenimento
def tela_estoque_func():
    tela_estoque = tk.Toplevel()
    tela_estoque.geometry("800x600")
    tela_estoque["bg"] = "#EE8507"
    tela_estoque.title("Estoque")
    icon_window = ImageTk.PhotoImage(file=CHAVEIRO_ICON)
    tela_estoque.iconbitmap(default=CHAVEIRO_ICON)
    tela_estoque.iconphoto(False, icon_window)

    # Estoque informações
    num_chave = tk.IntVar()
    nom_chave = tk.StringVar()
    quant_chave = tk.IntVar()
    val_chave = tk.DoubleVar()

    id_chave_retorno = cur.execute("SELECT id_chave FROM estoque")
    retorno_ultimo_id = id_chave_retorno.fetchall()[-1]
    print(retorno_ultimo_id[0])

    # Tela estoque
    image_estoque = Image.open("Tela_de_estoque.png")
    photo_estoque = ImageTk.PhotoImage(image_estoque)
    imagem_estoque = tk.Label(
        tela_estoque, width=800, height=600, image=photo_estoque, text="adcionando3"
    )
    imagem_estoque.image = photo_estoque
    imagem_estoque.pack()

    # Frames estoque
    cadastro_frame = tk.LabelFrame(
        imagem_estoque,
        width=250,
        height=390,
        relief="sunken",
        bd=4,
        bg="#E1834E",
        text="Cadastrar mercadoria",
        font="Latha 13",
    )
    cadastro_frame.place(x=30, y=30)

    estoque_frame = tk.LabelFrame(
        imagem_estoque,
        width=530,
        height=560,
        relief="sunken",
        bd=4,
        bg="#E1834E",
        text="Estoque",
        font="Latha 13",
    )
    estoque_frame.place(x=280, y=30)
    cadastro_frame.pack_propagate(False)
    # Botões estoque

    num_chave_lab = tk.Label(
        cadastro_frame, text="Número da chave", bg="#E1834E", font=DEFAULT_FONT
    ).place(x=0, y=40)
    nom_chave_lab = tk.Label(
        cadastro_frame, text="Nome da chave", bg="#E1834E", font=DEFAULT_FONT
    ).place(x=0, y=80)
    quant_chave_lab = tk.Label(
        cadastro_frame,
        text="Quantidade",
        bg="#E1834E",
        font=DEFAULT_FONT,
    ).place(x=0, y=120)
    val_chave_lab = tk.Label(
        cadastro_frame, text="Valor", bg="#E1834E", font=DEFAULT_FONT
    ).place(x=0, y=160)

    # Cadastro Entry

    num_chave_ent = tk.Entry(
        cadastro_frame,
        width=8,
        bd=4,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=num_chave,
        justify="center",
    )
    num_chave_ent.place(x=150, y=40)
    num_chave_ent.delete(0, tkc.END)

    nom_chave_ent = tk.Entry(
        cadastro_frame,
        width=8,
        bd=4,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=nom_chave,
        justify="center",
    )
    nom_chave_ent.place(x=150, y=80)

    quant_chave_ent = tk.Entry(
        cadastro_frame,
        width=8,
        bd=4,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=quant_chave,
        justify="center",
    )
    quant_chave_ent.place(x=150, y=120)
    quant_chave_ent.delete(0, tkc.END)

    val_chave_ent = tk.Entry(
        cadastro_frame,
        width=8,
        bd=4,
        relief="groove",
        bg="#3E362D",
        fg="#EEE3D5",
        font="Latha",
        textvariable=val_chave,
        justify="center",
    )
    val_chave_ent.place(x=150, y=160)
    val_chave_ent.delete(0, tkc.END)

    enviar_cadastro_est = tk.Button(
        cadastro_frame,
        width=10,
        height=1,
        text="Enviar",
        bd=3,
        relief="ridge",
        bg="#2DB00D",
        highlightbackground="#32FF00",
        activebackground="#80C270",
        command=lambda: estoque_analise(
            lista_estoque,
            retorno_ultimo_id,
            num_chave,
            nom_chave,
            quant_chave,
            val_chave,
        ),
    ).place(x=120, y=280)
    update_cadastro_est = tk.Button(
        cadastro_frame,
        width=10,
        height=1,
        text="Atualizar",
        bd=3,
        relief="ridge",
        bg="#FFFB07",
        highlightbackground="#F7FF00",
        activebackground="#FFD100",
        command=lambda: atualizar_estoque(
            lista_estoque, num_chave, nom_chave, quant_chave, val_chave
        ),
    ).place(x=120, y=240)

    scroll_y = tk.Scrollbar(estoque_frame, orient=tkc.VERTICAL, bg="#db8e46")

    style = ttk.Style(tela_estoque)
    style.configure("Treeview", background="#E1834E", fieldbackground="#E1834E")
    style.configure("Treeview.Heading", background="#db8e46")

    lista_estoque = ttk.Treeview(
        estoque_frame,
        height=23,
        columns=("id", "numero", "nome", "quantidade", "valor"),
        show="headings",
        yscrollcommand=scroll_y.set,
    )

    lista_estoque["displaycolumns"] = ("numero", "nome", "quantidade", "valor")

    scroll_y.pack(side=tkc.LEFT, fill=tkc.Y)

    lista_estoque.heading("id", text="Id")
    lista_estoque.heading("numero", text="Número")
    lista_estoque.heading("nome", text="Nome")
    lista_estoque.heading("quantidade", text="Quantidade")
    lista_estoque.heading("valor", text="Valor R$")

    lista_estoque.column("id", minwidth=0, anchor=tkc.CENTER)
    lista_estoque.column("numero", width=100)
    lista_estoque.column("nome", anchor=tkc.W, width=100)
    lista_estoque.column("quantidade", anchor=tkc.CENTER, width=100)
    lista_estoque.column("valor", anchor=tkc.CENTER, width=100)

    lista_estoque.pack(fill=tkc.BOTH, expand=True)

    # Selecionar produtos na lista
    lista_estoque.bind(
        "<ButtonRelease-1>",
        lambda eff: selecionar_item(
            eff,
            lista_estoque,
            num_chave_ent,
            nom_chave_ent,
            quant_chave_ent,
            val_chave_ent,
        ),
    )
    # Insert no Treeview
    retorno_id = cur.fetchone()
    cur.execute("SELECT * FROM estoque ORDER BY id_chave")
    select_estoque_ins = cur.fetchall()
    for item_estoque in select_estoque_ins:
        lista_estoque.insert(
            "",
            tkc.END,
            iid=item_estoque[0],
            values=(
                item_estoque[0],
                item_estoque[1],
                item_estoque[2],
                item_estoque[3],
                item_estoque[4],
            ),
        )
        conn.commit()

    delete_cadastro_est = tk.Button(
        cadastro_frame,
        width=10,
        height=1,
        text="Deletar",
        bd=3,
        relief="ridge",
        bg="#BE1A07",
        highlightbackground="#BE1A07",
        activebackground="#E57365",
        command=lambda: deletar_estoque(
            lista_estoque, num_chave_ent, nom_chave_ent, quant_chave_ent, val_chave_ent
        ),
    ).place(x=120, y=320)
    tela_estoque.mainloop()


def clear_entry_cliente(
    data_cliente_ent,
    cliente_cliente_ent,
    produto_combobox,
    quantidade_cliente_ent,
    valor_cliente_ent,
):
    data_cliente_ent.delete(0, tkc.END)
    cliente_cliente_ent.delete(0, tkc.END)
    produto_combobox.delete(0, tkc.END)
    quantidade_cliente_ent.delete(0, tkc.END)
    valor_cliente_ent.delete(0, tkc.END)


def estoque_analise(
    lista_estoque, retorno_ultimo_id, num_chave, nom_chave, quant_chave, val_chave
):
    if (
        num_chave.get() == None
        or nom_chave.get() == None
        or quant_chave.get() == None
        or val_chave.get() == None
    ):
        messagebox.showwarning(
            title=WARNING_MESSAGE,
            message="Você precisa preencher todos os campos para o cadastro.",
        )
    else:
        cadastrar_estoque(
            lista_estoque,
            retorno_ultimo_id,
            num_chave,
            nom_chave,
            quant_chave,
            val_chave,
        )


def clear_entry_est(num_chave_ent, nom_chave_ent, quant_chave_ent, val_chave_ent):
    num_chave_ent.delete(0, tkc.END)
    nom_chave_ent.delete(0, tkc.END)
    quant_chave_ent.delete(0, tkc.END)
    val_chave_ent.delete(0, tkc.END)


def selecionar_item(
    a, lista_estoque, num_chave_ent, nom_chave_ent, quant_chave_ent, val_chave_ent
):
    clear_entry_est(num_chave_ent, nom_chave_ent, quant_chave_ent, val_chave_ent)

    focar_item = lista_estoque.focus()
    item_tree = lista_estoque.item(focar_item)
    retorno_lista_item_tree = item_tree["values"]
    num_chave_ent.insert(0, retorno_lista_item_tree[1])
    nom_chave_ent.insert(0, retorno_lista_item_tree[2])
    quant_chave_ent.insert(0, retorno_lista_item_tree[3])
    val_chave_ent.insert(0, retorno_lista_item_tree[4])

    for item_lista in retorno_lista_item_tree:
        print(item_lista)


def cadastrar_estoque(
    lista_estoque, retorno_ultimo_id, num_chave, nom_chave, quant_chave, val_chave
):
    conn = sqlite3.connect(DEFAULT_DATABASE)
    cur = conn.cursor()
    retorno_id = cur.fetchone()
    retorno_ultimo_id_soma = retorno_ultimo_id[0]
    retorno_ultimo_id_soma += 1
    print(retorno_ultimo_id_soma)

    (
        cur.execute(
            "INSERT INTO estoque VALUES(?,?,?,?,?)",
            (
                retorno_id,
                num_chave.get(),
                nom_chave.get(),
                quant_chave.get(),
                val_chave.get(),
            ),
        ),
    )
    lista_estoque.insert(
        "",
        tkc.END,
        values=(
            retorno_ultimo_id_soma,
            num_chave.get(),
            nom_chave.get(),
            quant_chave.get(),
            val_chave.get(),
            val_chave.get(),
        ),
    )
    (conn.commit(),)


def atualizar_estoque(lista_estoque, num_chave, nom_chave, quant_chave, val_chave):
    conn = sqlite3.connect(DEFAULT_DATABASE)
    cur = conn.cursor()

    focar_item = lista_estoque.focus()
    retorno_focar_item = lista_estoque.item(focar_item)
    values_retorno_focar_item = retorno_focar_item["values"]
    print(values_retorno_focar_item[0])
    lista_estoque.item(
        focar_item,
        text="",
        values=(
            values_retorno_focar_item[0],
            num_chave.get(),
            nom_chave.get(),
            quant_chave.get(),
            val_chave.get(),
        ),
    )

    cur.execute(
        """UPDATE estoque SET
                num_chave=:num_chave_up,
                nom_chave=:nom_chave_up,
                quant_chave=:quant_chave_up,
                val_chave=:val_chave_up
                WHERE id_chave= :id_chave_up""",
        {
            "num_chave_up": num_chave.get(),
            "nom_chave_up": nom_chave.get(),
            "quant_chave_up": quant_chave.get(),
            "val_chave_up": val_chave.get(),
            "id_chave_up": values_retorno_focar_item[0],
        },
    )

    conn.commit()


def deletar_estoque(
    lista_estoque, num_chave_ent, nom_chave_ent, quant_chave_ent, val_chave_ent
):
    conn = sqlite3.connect(DEFAULT_DATABASE)
    cur = conn.cursor()

    focar_item = lista_estoque.focus()
    retorno_focar_item = lista_estoque.item(focar_item)
    values_retorno_focar_item = retorno_focar_item["values"]
    retorno_id = values_retorno_focar_item[0]
    print(values_retorno_focar_item)
    print(retorno_id)
    cur.execute("DELETE FROM estoque WHERE id_chave=?", (retorno_id,))

    conn.commit()

    for retorno_estoque_delete in values_retorno_focar_item:
        lista_estoque.delete(retorno_estoque_delete)
    clear_entry_est(num_chave_ent, nom_chave_ent, quant_chave_ent, val_chave_ent)


def selecionar_item_cliente(
    a,
    lista_cliente,
    data_cliente_ent,
    cliente_cliente_ent,
    produto_combobox,
    quantidade_cliente_ent,
    valor_cliente_ent,
):
    clear_entry_cliente(
        data_cliente_ent,
        cliente_cliente_ent,
        produto_combobox,
        quantidade_cliente_ent,
        valor_cliente_ent,
    )

    focar_item_cliente = lista_cliente.focus()
    item_tree_cliente = lista_cliente.item(focar_item_cliente)
    retorno_lista_item_tree_cliente = item_tree_cliente["values"]
    data_cliente_ent.insert(0, retorno_lista_item_tree_cliente[1])
    cliente_cliente_ent.insert(0, retorno_lista_item_tree_cliente[2])
    produto_combobox.insert(0, retorno_lista_item_tree_cliente[3])
    quantidade_cliente_ent.insert(0, retorno_lista_item_tree_cliente[4])
    valor_cliente_ent.insert(0, retorno_lista_item_tree_cliente[5])

    for item_lista_cliente in retorno_lista_item_tree_cliente:
        print(item_lista_cliente)


def atualizar_cliente(
    lista_cliente,
    data_cliente,
    cliente_cliente,
    produto_cliente,
    quantidade_cliente,
    valor_cliente,
):
    conn = sqlite3.connect(DEFAULT_DATABASE)
    cur = conn.cursor()

    focar_item_cliente = lista_cliente.focus()
    retorno_focar_item_cliente = lista_cliente.item(focar_item_cliente)
    values_retorno_focar_item_cliente = retorno_focar_item_cliente["values"]
    print(values_retorno_focar_item_cliente[0])
    lista_cliente.item(
        focar_item_cliente,
        text="",
        values=(
            values_retorno_focar_item_cliente[0],
            data_cliente.get(),
            cliente_cliente.get(),
            produto_cliente.get(),
            quantidade_cliente.get(),
            valor_cliente.get(),
        ),
    )

    cur.execute(
        """UPDATE clientes SET
                    data=:data_up,
                    cliente=:cliente_up,
                    produto=:produto_up,
                    quantidade=:quantidade_up,
                    valor=:valor_up
                    WHERE id_cliente= :id_cliente_up""",
        {
            "data_up": data_cliente.get(),
            "cliente_up": cliente_cliente.get(),
            "produto_up": produto_cliente.get(),
            "quantidade_up": quantidade_cliente.get(),
            "valor_up": valor_cliente.get(),
            "id_cliente_up": values_retorno_focar_item_cliente[0],
        },
    )

    conn.commit()


def deletar_cliente(
    lista_cliente,
    data_cliente_ent,
    cliente_cliente_ent,
    produto_combobox,
    quantidade_cliente_ent,
    valor_cliente_ent,
):
    conn = sqlite3.connect(DEFAULT_DATABASE)
    cur = conn.cursor()

    focar_item_cliente = lista_cliente.focus()
    retorno_focar_item_cliente = lista_cliente.item(focar_item_cliente)
    values_retorno_focar_item_cliente = retorno_focar_item_cliente["values"]
    retorno_id_cliente = values_retorno_focar_item_cliente[0]
    print(values_retorno_focar_item_cliente)
    print(retorno_id_cliente)
    cur.execute("DELETE FROM clientes WHERE id_cliente=?", (retorno_id_cliente,))

    conn.commit()
    conn.close()

    for retorno_cliente_delete in values_retorno_focar_item_cliente:
        lista_cliente.delete(retorno_cliente_delete)
    clear_entry_cliente(
        data_cliente_ent,
        cliente_cliente_ent,
        produto_combobox,
        quantidade_cliente_ent,
        valor_cliente_ent,
    )


# Relógio new_window
def clock(label_clock):
    BRA = timezone("Brazil/East")
    time = datetime.now(BRA)
    time_clock = time.strftime("%H:%M:%S")

    # Traduzir dia
    day_translate = time.strftime("%A")

    if day_translate == "Monday":
        day_translate = "Segunda"

    elif day_translate == "Tuesday":
        day_translate = "Terça"

    elif day_translate == "Wednesday":
        day_translate = "Quarta"

    elif day_translate == "Thursday":
        day_translate = "Quinta"

    elif day_translate == "Friday":
        day_translate = "Sexta"

    elif day_translate == "Saturday":
        day_translate = "Sábado"

    elif day_translate == "Sunday":
        day_translate = "Domingo"

    label_clock.config(text=time_clock + "\n" + day_translate)
    label_clock.after(200, clock, label_clock)


# Botões
usuario_entry = tk.Entry(
    window,
    width=23,
    bd=4,
    relief="groove",
    bg="#3E362D",
    fg="#EEE3D5",
    font="Latha",
    textvariable=usuario,
)
usuario_entry.place(x=185, y=55)
usuario_entry.focus()


senha_entry = tk.Entry(
    window,
    bd=3,
    width=23,
    relief="groove",
    bg="#3E362D",
    fg="#EEE3D5",
    font="Latha",
    show="*",
    textvariable=senha,
)
senha_entry.place(x=185, y=116)

enviar = tk.Button(
    window,
    width=7,
    height=1,
    text="Enviar",
    bd=3,
    relief="ridge",
    bg="#2DB00D",
    highlightbackground="#32FF00",
    activebackground="#80C270",
    command=analisar,
).place(x=306, y=150)

deletar = tk.Button(
    window,
    width=7,
    height=1,
    text="Apagar",
    bd=3,
    relief="ridge",
    pady=1,
    bg="#BE1A07",
    highlightbackground="#BE1A07",
    activebackground="#E57365",
).place(x=200, y=152)

window.mainloop()
