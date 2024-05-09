import flet as ft
import sqlite3
import datetime

class InserirModelo: #Funcional
    def __init__(self, page:ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color = {
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor = {
                ft.MaterialState.HOVERED:ft.colors.CYAN,
                ft.MaterialState.DEFAULT:ft.colors.AMBER,
            },
            padding = {
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text= 'Voltar', icon = ft.icons.ARROW_BACK_ROUNDED , style = x, on_click = self.voltar)
        btn_menu   = ft.ElevatedButton(text='Menu',icon=ft.icons.MENU, style = x, on_click= self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style= x, on_click = self.limpar)
        btn_submit = ft.ElevatedButton(text='Inserir', style= x, on_click= self.validacao)
        btn_fechar = ft.TextButton(text = 'Fechar', on_click = self.pop)

        # Pop Up
        self.ad1 = ft.AlertDialog(
            title= ft.Text(value = 'Alerta'),
            content = ft.Text(value = 'Preencher e/ou selecionar o(s) campo(s):\n'),
            actions = [ btn_fechar
            ],
            modal=True,
            )
        
        # Formulário
        last_modelo_id = self.get_last_modelo_id() 
        self.id_modelo = ft.TextField(
            label = 'ID Modelo',
            value= str(last_modelo_id + 1),
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            read_only=True,
        )

        self.motor = ft.TextField(
            label='Nome do motor',
            hint_text='Exemplo: Awsvts',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        
        self.cor = ft.Dropdown(
            label = 'Selecione a cor',
            options = [
                ft.dropdown.Option(key = 'Vermelha', text = 'Vermelha'),
                ft.dropdown.Option(key = 'Azul', text = 'Azul'),
                ft.dropdown.Option(key = 'Rosa', text = 'Rosa'),
                ft.dropdown.Option(key = 'Verde', text = 'Verde'),
                ft.dropdown.Option(key = 'Laranja', text = 'Laranja'),
                ft.dropdown.Option(key = 'Roxo', text = 'Roxo'),
                ft.dropdown.Option(key = 'Branca', text = 'Branca'),
                ft.dropdown.Option(key = 'Preta', text = 'Preta'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.formato = ft.Dropdown(
            label = 'Selecione o formato',
            options = [
                ft.dropdown.Option(key = 'Quadrado', text = 'Quadrado'),
                ft.dropdown.Option(key = 'Oval', text = 'Oval'),
                ft.dropdown.Option(key = 'Triangular', text = 'Triangular'),
                ft.dropdown.Option(key = 'Cilindro', text = 'Cilindro'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        
        
        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Container(
                    top= 350,
                    left= 810,
            
                    content = ft.Column(
                    controls = [
                        self.id_modelo,
                        self.motor,
                        self.cor,
                        self.formato,  
                    ],
                    spacing=15,
                )),  
                ft.Container(
                    top=750,
                    left=810,

                    content= ft.Row(
                        controls= [
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),   
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()

    # Método para pegar o último ID_nave
    def get_last_modelo_id(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('SELECT MAX(ID_Modelo) FROM Modelo')
            last_id = cur.fetchone()[0]
            return last_id if last_id else 0  # Retorna 0 se não houver nenhum ID de nave ainda  
 

    # Método para limpar
    def limpar(self, e):
        self.motor.value = ''
        self.motor.update()

        self.cor.value = None
        self.cor.update()

        self.formato.value = None
        self.formato.update()


    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.motor.value == '':
            campos_em_branco.append('Nome do motor')

        if self.cor.value == '':
            campos_em_branco.append('Cor')

        if self.formato.value == '':
            campos_em_branco.append('Formato')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
        # Todos os campos estão preenchidos, então podemos submeter os dados
            self.submeter()


    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()

    # Método para salvar o
    def submeter(self):
        try:
            # Conectar ao banco de dados
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                # Inserir os dados na tabela Modelo
                cur.execute('INSERT INTO Modelo (Cor, Formato, Motor) VALUES (?, ?, ?)',
                            (self.cor.value, self.formato.value, self.motor.value))
                # Commit para salvar as alterações
                con.commit()
                # Atualizar o campo id_modelo na interface gráfica
                self.id_modelo.value = str(self.get_last_modelo_id() + 1)
                

                # Limpar os campos após a inserção
                self.limpar(None)

                # Mostrar mensagem de sucesso
                self.ad1.content.value = 'Dados inseridos com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao inserir dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveMod(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class AlterarModelo: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click = self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Alterar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        # Pop Up
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_modelo = ft.TextField(
            label='ID Modelo',
            hint_text='Inserir ID Modelo',
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        
        self.cor = ft.Dropdown(
            label = 'Selecione a cor',
            options = [
                ft.dropdown.Option(key = 'Vermelha', text = 'Vermelha'),
                ft.dropdown.Option(key = 'Azul', text = 'Azul'),
                ft.dropdown.Option(key = 'Rosa', text = 'Rosa'),
                ft.dropdown.Option(key = 'Verde', text = 'Verde'),
                ft.dropdown.Option(key = 'Laranja', text = 'Laranja'),
                ft.dropdown.Option(key = 'Roxo', text = 'Roxo'),
                ft.dropdown.Option(key = 'Branca', text = 'Branca'),
                ft.dropdown.Option(key = 'Preta', text = 'Preta'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.formato = ft.Dropdown(
            label = 'Selecione o formato',
            options = [
                ft.dropdown.Option(key = 'Quadrado', text = 'Quadrado'),
                ft.dropdown.Option(key = 'Oval', text = 'Oval'),
                ft.dropdown.Option(key = 'Triangular', text = 'Triangular'),
                ft.dropdown.Option(key = 'Cilindro', text = 'Cilindro'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.motor = ft.TextField(
            label='Nome do motor',
            hint_text='Exemplo: Awsvts',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=ft.Column(
                        controls=[
                            self.id_modelo,
                            self.motor,
                            self.cor,
                            self.formato,
                        ],
                        spacing=15,
                    )),
                ft.Container(
                    top=750,
                    left=810,
                    content=ft.Row(
                        controls=[
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=95,
                    )
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x,on_click=self.pesquisar_nave,)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.id_modelo.value = ''
        self.id_modelo.update()

        self.motor.value = ''
        self.motor.read_only=True
        self.motor.update()

        self.cor.value = None
        self.cor.disabled=True
        self.cor.update()

        self.formato.value = None
        self.formato.disabled=True
        self.formato.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.motor.value == '':
            campos_em_branco.append('Nome do motor')

        if self.cor.value == '':
            campos_em_branco.append('Cor')

        if self.formato.value == '':
            campos_em_branco.append('Formato')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
        # Todos os campos estão preenchidos, então podemos submeter os dados
            self.submeter()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE Modelo
                    SET Cor = ?,
                    Formato = ?,
                    Motor = ?
                    WHERE ID_Modelo = ?
                    """,
                    (
                        self.cor.value,
                        self.formato.value, 
                        self.motor.value,
                        self.id_modelo.value,
                    ),
                )
                con.commit()
                # Limpar os campos após a inserção
                self.limpar(None)

                self.ad1.content.value = 'Dados alterados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao alterar dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    #Pesquisar valor
    def pesquisar_nave(self, e):
        id_modelo_pesquisa = self.id_modelo.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT Cor, Formato, Motor
                    FROM Modelo
                    WHERE ID_Modelo = ?
                    """,
                    (id_modelo_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    # Preenchendo o dropdown cor
                    self.cor.value = result[0]  
                    self.cor.disabled = False
                    self.cor.update()
                    self.formato.value = result[1] 
                    self.formato.disabled = False
                    self.formato.update()
                    # Preenchendo o campo do nome do motor
                    self.motor.value = result[2]
                    self.motor.read_only = False
                    self.motor.update()

                    self.page.update()
                else:
                    self.page.dialog = self.ad2
                    self.ad2.open = True
                    self.page.update()           
        except:
            pass
    # Ligação para Menu
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveMod(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class EliminarModelo: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click = self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Eliminar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        # Pop Up
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_modelo = ft.TextField(
            label='ID Modelo',
            hint_text='Inserir ID Modelo',
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        
        self.cor = ft.Dropdown(
            label = 'Selecione a cor',
            options = [
                ft.dropdown.Option(key = 'Vermelha', text = 'Vermelha'),
                ft.dropdown.Option(key = 'Azul', text = 'Azul'),
                ft.dropdown.Option(key = 'Rosa', text = 'Rosa'),
                ft.dropdown.Option(key = 'Verde', text = 'Verde'),
                ft.dropdown.Option(key = 'Laranja', text = 'Laranja'),
                ft.dropdown.Option(key = 'Roxo', text = 'Roxo'),
                ft.dropdown.Option(key = 'Branca', text = 'Branca'),
                ft.dropdown.Option(key = 'Preta', text = 'Preta'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.formato = ft.Dropdown(
            label = 'Selecione o formato',
            options = [
                ft.dropdown.Option(key = 'Quadrado', text = 'Quadrado'),
                ft.dropdown.Option(key = 'Oval', text = 'Oval'),
                ft.dropdown.Option(key = 'Triangular', text = 'Triangular'),
                ft.dropdown.Option(key = 'Cilindro', text = 'Cilindro'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )


        self.motor = ft.TextField(
            label='Nome do motor',
            hint_text='Exemplo: Awsvts',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=ft.Column(
                        controls=[
                            self.id_modelo,
                            self.motor,
                            self.cor,
                            self.formato,
                        ],
                        spacing=15,
                    )),
                ft.Container(
                    top=750,
                    left=810,
                    content=ft.Row(
                        controls=[
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=95,
                    )
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x,on_click=self.pesquisar_nave,)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.id_modelo.value = ''
        self.id_modelo.update()

        self.motor.value = ''
        self.motor.update()

        self.cor.value = None
        self.cor.update()

        self.formato.value = None
        self.formato.update()

    # Método para validar
    def validacao(self, e):
        self.submeter()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                cur.execute(
                    """
                    DELETE FROM Modelo
                    WHERE ID_Modelo = ?
                    """,
                    (
                        self.id_modelo.value,
                    ),
                )
                con.commit()
                # Limpar os campos após a eliminação
                self.limpar(None)

                self.ad1.content.value = 'Dados Eliminados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

        except Exception as ex:
            self.ad1.content.value = 'Erro desconhecido ao eliminar dados.'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_nave(self, e):
        id_modelo_pesquisa = self.id_modelo.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT Cor, Formato, Motor
                    FROM Modelo
                    WHERE ID_Modelo = ?
                    """,
                    (id_modelo_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    # Preenchendo o dropdown cor
                    self.cor.value = result[0]  
                    self.cor.update()
                    self.formato.value = result[1] 
                    self.formato.update()
                    self.motor.value = result[2]
                    self.motor.update()

                    self.page.update()
                else:
                    self.page.dialog = self.ad2
                    self.ad2.open = True
                    self.page.update()           
        except:
            pass
     # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveMod(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class ListarModelo: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.page.auto_scroll=True
        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        
        self.listar = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Modelo")),
                ft.DataColumn(ft.Text("Cor")),
                ft.DataColumn(ft.Text("Formato")),
                ft.DataColumn(ft.Text("Motor")),
            ],
            rows=[],  # Inicialmente vazia, os dados serão preenchidos posteriormente
        )
        self.preencher_tabela()

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        self.btn_voltar,
                        self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=self.listar,  # Adicionando a DataTable à página
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para preencher a DataTable com os dados do banco de dados
    def preencher_tabela(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT ID_Modelo, Cor, Formato, Motor
                    FROM Modelo
                    """
                )
                data = cur.fetchall()
                # Limpar qualquer dado anterior
                self.listar.rows.clear()
                # Preencher a tabela com os novos dados
                for row in data:
                    self.listar.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]))
        except sqlite3.Error as e:
            print("Erro ao recuperar dados da tabela Modelo:", e)

    # Ligação para o Menu Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNaveMod
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveMod(self.page)
        voltar.main_page()

    def main_page(self):
        pass

class InserirNave: #Funcional
    def __init__(self, page:ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color = {
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor = {
                ft.MaterialState.HOVERED:ft.colors.CYAN,
                ft.MaterialState.DEFAULT:ft.colors.AMBER,
            },
            padding = {
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text= 'Voltar', icon = ft.icons.ARROW_BACK_ROUNDED , style = x, on_click = self.voltar)
        btn_menu   = ft.ElevatedButton(text='Menu',icon=ft.icons.MENU, style = x, on_click= self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style= x, on_click = self.limpar)
        btn_submit = ft.ElevatedButton(text='Inserir', style= x, on_click= self.validacao)
        btn_fechar = ft.TextButton(text = 'Fechar', on_click = self.pop)

        # Pop Up
        self.ad1 = ft.AlertDialog(
            title= ft.Text(value = 'Alerta'),
            content = ft.Text(value = 'Preencher e/ou selecionar o(s) campo(s):\n'),
            actions = [ btn_fechar
            ],
            modal=True,
            )
        
        # Formulário
        last_nave_id = self.get_last_nave_id() 
        self.id_nave = ft.TextField(
            label = 'ID Nave',
            value= str(last_nave_id + 1),
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            read_only=True,
        )

        self.quant_max_pas = ft.TextField(
            label='Quantidade máxima de passageiros',
            hint_text='Inserir valor de 0 a 99',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=2,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        
        self.deslocamento = ft.Dropdown(
            label = 'Selecione o deslocamento',
            options = [
                ft.dropdown.Option(key = 'Planeta local', text = 'Planeta local'),
                ft.dropdown.Option(key = 'Entre planetas', text = 'Entre planetas'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.nave_roubada = ft.Dropdown(
            label = 'Nave roubada?',
            options = [
                ft.dropdown.Option(key = 'Sim', text = 'Sim'),
                ft.dropdown.Option(key = 'Não', text = 'Não'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        self.id_modelo = ft.TextField(
            label = 'ID modelo da nave',
            hint_text = 'Ex: 1',
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            input_filter= ft.NumbersOnlyInputFilter(),
        )
        
        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Container(
                    top= 350,
                    left= 810,
            
                    content = ft.Column(
                    controls = [
                        self.id_nave,
                        self.quant_max_pas,
                        self.deslocamento,
                        self.nave_roubada,
                        self.id_modelo, 
                         
                    ],
                    spacing=15,
                )),  
                ft.Container(
                    top=750,
                    left=810,

                    content= ft.Row(
                        controls= [
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),   
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()

    # Método para pegar o último ID_nave
    def get_last_nave_id(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('SELECT MAX(IDNave) FROM Nave')
            last_id = cur.fetchone()[0]
            return last_id if last_id else 0  # Retorna 0 se não houver nenhum ID de nave ainda  
 

    # Método para limpar
    def limpar(self, e):
        self.quant_max_pas.value = ''
        self.quant_max_pas.update()

        self.deslocamento.value = ''
        self.deslocamento.update()

        self.nave_roubada.value = ''
        self.nave_roubada.update()

        self.id_modelo.value = ''
        self.id_modelo.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.quant_max_pas.value == '':
            campos_em_branco.append('Quantidade máxima de passageiros')

        if self.deslocamento.value == '':
            campos_em_branco.append('Deslocamento')

        if self.nave_roubada.value == '':
            campos_em_branco.append('Nave Roubada')

        if self.id_modelo.value == '':
            campos_em_branco.append('ID modelo da nave')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
        # Verificar se o ID_Modelo existe na tabela Modelo
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            try:
                cur.execute("SELECT COUNT(*) FROM Modelo WHERE ID_Modelo = ?", (self.id_modelo.value,))
                count = cur.fetchone()[0]

                if count == 0:
                    # Se o ID_Modelo não existir na tabela Modelo, exibir uma mensagem de erro
                    self.ad1.content.value = "O ID do modelo da nave não existe"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
                    return
                else:
                    self.submeter()
            except:
                pass
            finally:
                con.close()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()

    # Método para salvar
    def submeter(self):

        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                # Traduzir os valores dos dropdowns para os textos correspondentes
                deslocamento_texto = 'Planeta local' if self.deslocamento.value == '1' else 'Entre planetas'
                nave_roubada_texto = 'Sim' if self.nave_roubada.value == '1' else 'Não'

                # Inserir os dados na tabela Nave
                cur.execute('INSERT INTO Nave (QuantMaxPassageiros, Deslocamento, NaveRoubada, ID_Modelo) VALUES (?, ?, ?, ?)',
                            (self.quant_max_pas.value, self.deslocamento.value, self.nave_roubada.value, self.id_modelo.value))
                # Commit para salvar as alterações
                con.commit()

                # Atualizar o id_nave após a inserção4
                self.id_nave.value = str(self.get_last_nave_id() + 1)

                # Limpar os campos após a inserção
                self.limpar(None)

                # Mostrar mensagem de sucesso
                self.ad1.content.value = 'Dados inseridos com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao inserir dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveDoc(self.page)
        voltar.main_page()

    def main_page(self):
        pass    
class AlterarNave: #Funcional

    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click = self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Alterar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        # Pop Up
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_nave = ft.TextField(
            label='ID Nave',
            hint_text='Inserir ID Nave',
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )

        self.quant_max_pas = ft.TextField(
            label='Quantidade máxima de passageiros',
            hint_text='Inserir valor de 1 a 99',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=2,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.deslocamento = ft.Dropdown(
            label = 'Selecione o deslocamento',
            options = [
                ft.dropdown.Option(key = 'Planeta local', text = 'Planeta local'),
                ft.dropdown.Option(key = 'Entre planetas', text = 'Entre planetas'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.nave_roubada = ft.Dropdown(
            label = 'Nave roubada?',
            options = [
                ft.dropdown.Option(key = 'Sim', text = 'Sim'),
                ft.dropdown.Option(key = 'Não', text = 'Não'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.id_modelo = ft.TextField(
            label='ID modelo da nave',
            hint_text='Inserir ID Modelo',
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            input_filter=ft.NumbersOnlyInputFilter(),
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=ft.Column(
                        controls=[
                            self.id_nave,
                            self.quant_max_pas,
                            self.deslocamento,
                            self.nave_roubada,
                            self.id_modelo,
                        ],
                        spacing=15,
                    )),
                ft.Container(
                    top=750,
                    left=810,
                    content=ft.Row(
                        controls=[
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=95,
                    )
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x,on_click=self.pesquisar_nave,)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.id_nave.value = ''
        self.id_nave.update()

        self.quant_max_pas.value = ''
        self.quant_max_pas.read_only=True
        self.quant_max_pas.update()

        self.deslocamento.value = None
        self.deslocamento.disabled=True
        self.deslocamento.update()

        self.nave_roubada.value = None
        self.nave_roubada.disabled=True
        self.nave_roubada.update()

        self.id_modelo.value = ''
        self.id_modelo.read_only=True
        self.id_modelo.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.id_nave.value == '':
            campos_em_branco.append('ID Nave')

        if self.quant_max_pas.value == '':
            campos_em_branco.append('Quantidade máxima de passageiros')

        if self.deslocamento.value == '':
            campos_em_branco.append('Deslocamento')

        if self.nave_roubada.value == '':
            campos_em_branco.append('Nave Roubada')

        if self.id_modelo.value == '':
            campos_em_branco.append('ID modelo da nave')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
            # Verificar se o ID_Modelo existe na tabela Modelo
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            try:
                cur.execute("SELECT COUNT(*) FROM Modelo WHERE ID_Modelo = ?", (self.id_modelo.value,))
                count = cur.fetchone()[0]

                if count == 0:
                    # Se o ID_Modelo não existir na tabela Modelo, exibir uma mensagem de erro
                    self.ad1.content.value = "O ID do modelo da nave não existe"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
                    return
                else:
                    self.submeter()
            except:
                pass
            finally:
                con.close()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE Nave
                    SET QuantMaxPassageiros = ?,
                        Deslocamento = ?,
                        NaveRoubada = ?,
                        ID_Modelo = ?
                    WHERE IDNave = ?
                    """,
                    (
                        self.quant_max_pas.value,
                        self.deslocamento.value,
                        self.nave_roubada.value,
                        self.id_modelo.value,
                        self.id_nave.value,
                    ),
                )
                con.commit()
                # Limpar os campos após a inserção
                self.limpar(None)

                self.ad1.content.value = 'Dados alterados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao alterar dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_nave(self, e):
        id_nave_pesquisa = self.id_nave.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT QuantMaxPassageiros, Deslocamento, NaveRoubada, ID_Modelo
                    FROM Nave
                    WHERE IDNave = ?
                    """,
                    (id_nave_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    self.quant_max_pas.value = result[0]
                    self.quant_max_pas.read_only=False
                    self.quant_max_pas.update()
                    
                    self.deslocamento.value = result[1]
                    self.deslocamento.disabled=False
                    self.deslocamento.update()
                    
                    self.nave_roubada.value = result[2]
                    self.nave_roubada.disabled=False
                    self.nave_roubada.update()

                    self.id_modelo.value = result[3]
                    self.id_modelo.read_only=False
                    self.id_modelo.update()
                    self.page.update()
                else:
                    self.page.dialog = self.ad2
                    self.ad2.open = True
                    self.page.update()           
        except:
            pass

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveDoc(self.page)
        voltar.main_page()

    def main_page(self):
        pass 
class EliminarNave: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click = self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Eliminar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
       
        # Pop Up
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_nave = ft.TextField(
            label='ID Nave',
            hint_text='Inserir ID Nave',
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        
        self.quant_max_pas = ft.TextField(
            label='Quantidade máxima de passageiros',
            hint_text='Inserir valor de 1 a 99',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=2,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.deslocamento = ft.Dropdown(
            label = 'Selecione o deslocamento',
            options = [
                ft.dropdown.Option(key = 'Planeta local', text = 'Planeta local'),
                ft.dropdown.Option(key = 'Entre planetas', text = 'Entre planetas'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.nave_roubada = ft.Dropdown(
            label = 'Nave roubada?',
            options = [
                ft.dropdown.Option(key = 'Sim', text = 'Sim'),
                ft.dropdown.Option(key = 'Não', text = 'Não'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.id_modelo = ft.TextField(
            label='ID modelo da nave',
            hint_text='Inserir ID Modelo',
            height=60,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            input_filter=ft.NumbersOnlyInputFilter(),
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=ft.Column(
                        controls=[
                            self.id_nave,
                            self.quant_max_pas,
                            self.deslocamento,
                            self.nave_roubada,
                            self.id_modelo,
                        ],
                        spacing=15,
                    )),
                ft.Container(
                    top=750,
                    left=810,
                    content=ft.Row(
                        controls=[
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=95,
                    )
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x,on_click=self.pesquisar_nave,)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.id_nave.value = ''
        self.id_nave.update()

        self.quant_max_pas.value = ''
        self.quant_max_pas.update()

        self.deslocamento.value = None
        self.deslocamento.update()

        self.nave_roubada.value = None
        self.nave_roubada.update()

        self.id_modelo.value = ''
        self.id_modelo.update()

    # Método para validar
    def validacao(self, e):
        self.submeter()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                cur.execute(
                    """
                    DELETE FROM Nave
                    WHERE IDNave = ?
                    """,
                    (
                        self.id_nave.value,
                    ),
                )
                con.commit()
                # Limpar os campos após a eliminação
                self.limpar(None)

                self.ad1.content.value = 'Dados Eliminados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

        except Exception as ex:
            self.ad1.content.value = 'Erro desconhecido ao eliminar dados.'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_nave(self, e):
        id_nave_pesquisa = self.id_nave.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT QuantMaxPassageiros, Deslocamento, NaveRoubada, ID_Modelo
                    FROM Nave
                    WHERE IDNave = ?
                    """,
                    (id_nave_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    self.quant_max_pas.value = result[0]
                    self.deslocamento.value = result[1] 
                    self.nave_roubada.value = result[2] 
                    self.id_modelo.value = result[3]
                    self.page.update()
                else:
                    self.page.dialog = self.ad2
                    self.ad2.open = True
                    self.page.update()           
        except:
            pass
     # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveDoc(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class ListarNave: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.page.auto_scroll=True
        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click = self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        


        # Formulário
        self.listar = ft.DataTable(
            
            columns=[
                ft.DataColumn(ft.Text("ID Nave")),
                ft.DataColumn(ft.Text("Quantidade Máxima de Passageiros")),
                ft.DataColumn(ft.Text("Tipo de Deslocamento")),
                ft.DataColumn(ft.Text("Nave Roubada")),
                ft.DataColumn(ft.Text("ID Modelo")),
            ],
            rows=[],  # Inicialmente vazia, os dados serão preenchidos posteriormente
        )
        self.preencher_tabela()
        
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        self.btn_voltar,
                        self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=500,
                    content=self.listar,  # Adicionando a DataTable à página
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()
    # Método para preencher a DataTable com os dados do banco de dados
    def preencher_tabela(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT IDNave, QuantMaxPassageiros, Deslocamento, NaveRoubada, ID_Modelo
                    FROM Nave
                    """
                )
                data = cur.fetchall()
                # Limpar qualquer dado anterior
                self.listar.rows.clear()
                # Preencher a tabela com os novos dados
                for row in data:
                    self.listar.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]))
        except sqlite3.Error as e:
            print("Erro ao recuperar dados da tabela Modelo:", e)

     # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaNaveDoc(self.page)
        voltar.main_page()

    def main_page(self):
        pass

class InserirAparencia: #Funcional
    def __init__(self, page:ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        
        #self.page.auto_scroll = True,
        
        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color = {
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor = {
                ft.MaterialState.HOVERED:ft.colors.CYAN,
                ft.MaterialState.DEFAULT:ft.colors.AMBER,
            },
            padding = {
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text= 'Voltar', icon = ft.icons.ARROW_BACK_ROUNDED , style = x, on_click = self.voltar)
        btn_menu   = ft.ElevatedButton(text='Menu',icon=ft.icons.MENU, style = x, on_click= self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style= x, on_click = self.limpar)
        btn_submit = ft.ElevatedButton(text='Inserir', style= x, on_click= self.validacao)
        btn_fechar = ft.TextButton(text = 'Fechar', on_click = self.pop)

        # Pop Up
        self.ad1 = ft.AlertDialog(
            title= ft.Text(value = 'Alerta'),
            content = ft.Text(value = 'Preencher e/ou selecionar o(s) campo(s):\n'),
            actions = [ btn_fechar
            ],
            modal=True,
            )
        
        # Formulário
        
        self.especie = ft.TextField(
            label = 'Espécie',
            hint_text='Exemplo: Humano',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            value= '',
            height=70,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        
        self.cor = ft.Dropdown(
            label = 'Selecione a cor da pele',
            options = [
                ft.dropdown.Option(key = 'Vermelha', text = 'Vermelha'),
                ft.dropdown.Option(key = 'Azul', text = 'Azul'),
                ft.dropdown.Option(key = 'Rosa', text = 'Rosa'),
                ft.dropdown.Option(key = 'Verde', text = 'Verde'),
                ft.dropdown.Option(key = 'Laranja', text = 'Laranja'),
                ft.dropdown.Option(key = 'Roxa', text = 'Roxo'),
                ft.dropdown.Option(key = 'Branca', text = 'Branca'),
                ft.dropdown.Option(key = 'Preta', text = 'Preta'),
                ft.dropdown.Option(key = 'Amarela', text = 'Amarela'),
            ],
            filled=True,
            width=140,
            height=70,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_braco = ft.TextField(
            label='Quantidade de braços',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_maos = ft.TextField(
            label='Quantidade de mãos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_pernas = ft.TextField(
            label='Quantidade de pernas',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_pes = ft.TextField(
            label='Quantidade de pés',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
           width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_cabecas = ft.TextField(
            label='Quantidade de cabeças',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_olhos = ft.TextField(
            label='Quantidade de olhos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_chifres = ft.TextField(
            label='Quantidade de chifres',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_caudas = ft.TextField(
            label='Quantidade de caudas',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        self.quant_tentaculos = ft.TextField(
            label='Quantidade de tentáculos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        
        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Column(
                    
                    controls = [
                        self.especie,
                        self.cor,
                        self.quant_braco,
                        self.quant_maos,
                        self.quant_pernas, 
                        self.quant_pes, 
                    ],
                    spacing=5,
                    auto_scroll = True,
                    top= 350,
                    left= 810,
                ), 
                ft.Column(
                    
                    controls = [
                        
                        
                        self.quant_cabecas,
                        self.quant_olhos,
                        self.quant_chifres,
                        self.quant_caudas,
                        self.quant_tentaculos,
                    ],
                    spacing=5,
                    top= 434,
                    left= 980,
                ),
                ft.Container(
                    top=815,
                    left=830,

                    content= ft.Row(
                        controls= [
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),   
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.especie.value = ''
        self.especie.update()

        self.cor.value = None
        self.cor.update()

        self.quant_braco.value = ''
        self.quant_braco.update()

        self.quant_maos.value = ''
        self.quant_maos.update()

        self.quant_pernas.value = ''
        self.quant_pernas.update()        

        self.quant_pes.value = ''
        self.quant_pes.update()

        self.quant_cabecas.value = ''
        self.quant_cabecas.update()

        self.quant_olhos.value = ''
        self.quant_olhos.update()

        self.quant_chifres.value = ''
        self.quant_chifres.update()

        self.quant_caudas.value = ''
        self.quant_caudas.update()

        self.quant_tentaculos.value = ''
        self.quant_tentaculos.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.especie.value == '':
            campos_em_branco.append('Espécie')

        if self.cor.value == '':
            campos_em_branco.append('Cor da pele')

        if self.quant_braco.value == '':
            campos_em_branco.append('Quantidade de braços')

        if self.quant_maos.value == '':
            campos_em_branco.append('Quantidade de mãos')

        if self.quant_pernas.value == '':
            campos_em_branco.append('Quantidade de pernas')

        if self.quant_pes.value == '':
            campos_em_branco.append('Quantidade de pés')

        if self.quant_cabecas.value == '':
            campos_em_branco.append('Quantidade de cabeças')

        if self.quant_olhos.value == '':
            campos_em_branco.append('Quantidade de olhos')

        if self.quant_chifres.value == '':
            campos_em_branco.append('Quantidade de chifres')

        if self.quant_caudas.value == '':
            campos_em_branco.append('Quantidade de caudas')

        if self.quant_tentaculos.value == '':
            campos_em_branco.append('Quantidade de tentáculos')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
        # Todos os campos estão preenchidos, então podemos submeter os dados
            self.submeter()


    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()

    # Método para salvar o
    def submeter(self):
        try:
            # Conectar ao banco de dados
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                # Inserir os dados na tabela Aparencia
                cur.execute('INSERT INTO Aparencia (Especie, CorPele, QuantBracos, QuantMaos, QuantPernas, QuantPes, QuantCabecas, QuantOlhos, QuantChifres, QuantCaudas, QuantTentaculos) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (self.especie.value, self.cor.value, self.quant_braco.value, self.quant_maos.value, self.quant_pernas.value, self.quant_pes.value, self.quant_cabecas.value, self.quant_olhos.value, self.quant_chifres.value, self.quant_caudas.value, self.quant_tentaculos.value))
                # Commit para salvar as alterações
                con.commit()
                # Limpar os campos após a inserção
                self.limpar(None)

                # Mostrar mensagem de sucesso
                self.ad1.content.value = 'Dados inseridos com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao inserir dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentApa(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class AlterarAparencia: #Funcional

    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Alterar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        # Pop Up
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.especie = ft.TextField(
            label = 'Espécie',
            hint_text='Exemplo: Humano',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            value= '',
            height=70,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        
        self.cor = ft.Dropdown(
            label = 'Selecione a cor da pele',
            options = [
                ft.dropdown.Option(key = 'Vermelha', text = 'Vermelha'),
                ft.dropdown.Option(key = 'Azul', text = 'Azul'),
                ft.dropdown.Option(key = 'Rosa', text = 'Rosa'),
                ft.dropdown.Option(key = 'Verde', text = 'Verde'),
                ft.dropdown.Option(key = 'Laranja', text = 'Laranja'),
                ft.dropdown.Option(key = 'Roxa', text = 'Roxo'),
                ft.dropdown.Option(key = 'Branca', text = 'Branca'),
                ft.dropdown.Option(key = 'Preta', text = 'Preta'),
                ft.dropdown.Option(key = 'Amarela', text = 'Amarela'),
            ],
            filled=True,
            width=140,
            height=70,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            disabled=True,
        )
        
        self.quant_braco = ft.TextField(
            label='Quantidade de braços',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_maos = ft.TextField(
            label='Quantidade de mãos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_pernas = ft.TextField(
            label='Quantidade de pernas',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_pes = ft.TextField(
            label='Quantidade de pés',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
           width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_cabecas = ft.TextField(
            label='Quantidade de cabeças',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_olhos = ft.TextField(
            label='Quantidade de olhos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_chifres = ft.TextField(
            label='Quantidade de chifres',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_caudas = ft.TextField(
            label='Quantidade de caudas',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_tentaculos = ft.TextField(
            label='Quantidade de tentáculos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Column(
                    
                    controls = [
                        self.especie,
                        self.cor,
                        self.quant_braco,
                        self.quant_maos,
                        self.quant_pernas, 
                        self.quant_pes, 
                    ],
                    spacing=5,
                    auto_scroll = True,
                    top= 350,
                    left= 810,
                ), 
                ft.Column(
                    
                    controls = [
                        self.quant_cabecas,
                        self.quant_olhos,
                        self.quant_chifres,
                        self.quant_caudas,
                        self.quant_tentaculos,
                    ],
                    spacing=5,
                    top= 434,
                    left= 980,
                ),
                ft.Container(
                    top=815,
                    left=830,

                    content= ft.Row(
                        controls= [
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x,on_click=self.pesquisar_especie,)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.especie.value = ''
        self.especie.update()

        self.cor.value = None
        self.cor.disabled=True
        self.cor.update()

        self.quant_braco.value = ''
        self.quant_braco.read_only=True
        self.quant_braco.update()

        self.quant_maos.value = ''
        self.quant_maos.read_only=True
        self.quant_maos.update()

        self.quant_pernas.value = ''
        self.quant_pernas.read_only=True
        self.quant_pernas.update()        

        self.quant_pes.value = ''
        self.quant_pes.read_only=True
        self.quant_pes.update()

        self.quant_cabecas.value = ''
        self.quant_cabecas.read_only=True
        self.quant_cabecas.update()

        self.quant_olhos.value = ''
        self.quant_olhos.read_only=True
        self.quant_olhos.update()

        self.quant_chifres.value = ''
        self.quant_chifres.read_only=True
        self.quant_chifres.update()

        self.quant_caudas.value = ''
        self.quant_caudas.read_only=True
        self.quant_caudas.update()

        self.quant_tentaculos.value = ''
        self.quant_tentaculos.read_only=True
        self.quant_tentaculos.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.especie.value == '':
            campos_em_branco.append('Espécie')

        if self.cor.value == '':
            campos_em_branco.append('Cor da pele')

        if self.quant_braco.value == '':
            campos_em_branco.append('Quantidade de braços')

        if self.quant_maos.value == '':
            campos_em_branco.append('Quantidade de mãos')

        if self.quant_pernas.value == '':
            campos_em_branco.append('Quantidade de pernas')

        if self.quant_pes.value == '':
            campos_em_branco.append('Quantidade de pés')

        if self.quant_cabecas.value == '':
            campos_em_branco.append('Quantidade de cabeças')

        if self.quant_olhos.value == '':
            campos_em_branco.append('Quantidade de olhos')

        if self.quant_chifres.value == '':
            campos_em_branco.append('Quantidade de chifres')

        if self.quant_caudas.value == '':
            campos_em_branco.append('Quantidade de caudas')

        if self.quant_tentaculos.value == '':
            campos_em_branco.append('Quantidade de tentáculos')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
        # Todos os campos estão preenchidos, então podemos submeter os dados
            self.submeter()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE Aparencia
                    SET CorPele=?, QuantBracos=?, QuantMaos=?, QuantPernas=?, QuantPes=?, QuantCabecas=?, QuantOlhos=?, QuantChifres=?, QuantCaudas=?, QuantTentaculos=?
                    WHERE Especie=?
                    """,
                    (self.cor.value, self.quant_braco.value, self.quant_maos.value, self.quant_pernas.value, self.quant_pes.value, self.quant_cabecas.value, self.quant_olhos.value, self.quant_chifres.value, self.quant_caudas.value, self.quant_tentaculos.value,self.especie.value,)
                )
                con.commit()
                # Limpar os campos após a inserção
                self.limpar(None)

                self.ad1.content.value = 'Dados alterados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao alterar dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()


    # Método para abrir o menu
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    def pesquisar_especie(self, e):
        especie_pesquisa = self.especie.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT CorPele, QuantBracos, QuantMaos, QuantPernas, QuantPes, QuantCabecas, QuantOlhos, QuantChifres, QuantCaudas, QuantTentaculos
                    FROM Aparencia
                    WHERE Especie = ?
                    """,
                    (especie_pesquisa,),
                )
                result = cur.fetchone()
                if result:                    
                # Atualizar os valores dos controles com os dados da pesquisa
                    self.cor.value = result[0]
                    self.cor.disabled=False
                    self.cor.update()

                    self.quant_braco.value = result[1]
                    self.quant_braco.read_only=False
                    self.quant_braco.update()

                    self.quant_maos.value = result[2]
                    self.quant_maos.read_only=False
                    self.quant_maos.update()

                    self.quant_pernas.value = result[3]
                    self.quant_pernas.read_only=False
                    self.quant_pernas.update() 

                    self.quant_pes.value = result[4]
                    self.quant_pes.read_only=False
                    self.quant_pes.update()
                    
                    self.quant_cabecas.value = result[5]
                    self.quant_cabecas.read_only=False
                    self.quant_cabecas.update()
                    
                    self.quant_olhos.value = result[6]
                    self.quant_olhos.read_only=False
                    self.quant_olhos.update()
                    
                    self.quant_chifres.value = result[7]
                    self.quant_chifres.read_only=False
                    self.quant_chifres.update()
                    
                    self.quant_caudas.value = result[8]
                    self.quant_caudas.read_only=False
                    self.quant_caudas.update()
                    
                    self.quant_tentaculos.value = result[9]
                    self.quant_tentaculos.read_only=False
                    self.quant_tentaculos.update()
                    
                    self.page.update()
                else:
                    self.page.dialog = self.ad2
                    self.ad2.open = True
                    self.page.update()           
        except:
            pass
    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaIdentApa
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentApa(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class EliminarAparencia: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click = self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Eliminar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        # Pop Up
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.especie = ft.TextField(
            label = 'Espécie',
            hint_text='Exemplo: Humano',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            value= '',
            height=70,
            width=300,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        
        self.cor = ft.Dropdown(
            label = 'Selecione a cor da pele',
            options = [
                ft.dropdown.Option(key = 'Vermelha', text = 'Vermelha'),
                ft.dropdown.Option(key = 'Azul', text = 'Azul'),
                ft.dropdown.Option(key = 'Rosa', text = 'Rosa'),
                ft.dropdown.Option(key = 'Verde', text = 'Verde'),
                ft.dropdown.Option(key = 'Laranja', text = 'Laranja'),
                ft.dropdown.Option(key = 'Roxa', text = 'Roxo'),
                ft.dropdown.Option(key = 'Branca', text = 'Branca'),
                ft.dropdown.Option(key = 'Preta', text = 'Preta'),
                ft.dropdown.Option(key = 'Amarela', text = 'Amarela'),
            ],
            filled=True,
            width=140,
            height=70,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            disabled=True,
        )
        
        self.quant_braco = ft.TextField(
            label='Quantidade de braços',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_maos = ft.TextField(
            label='Quantidade de mãos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_pernas = ft.TextField(
            label='Quantidade de pernas',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_pes = ft.TextField(
            label='Quantidade de pés',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
           width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_cabecas = ft.TextField(
            label='Quantidade de cabeças',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_olhos = ft.TextField(
            label='Quantidade de olhos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_chifres = ft.TextField(
            label='Quantidade de chifres',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_caudas = ft.TextField(
            label='Quantidade de caudas',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        self.quant_tentaculos = ft.TextField(
            label='Quantidade de tentáculos',
            hint_text='Inserir valor de 0 a 999',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=3,
            width=140,
            height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Column(
                    
                    controls = [
                        self.especie,
                        self.cor,
                        self.quant_braco,
                        self.quant_maos,
                        self.quant_pernas, 
                        self.quant_pes, 
                    ],
                    spacing=5,
                    auto_scroll = True,
                    top= 350,
                    left= 810,
                ), 
                ft.Column(
                    
                    controls = [
                        self.quant_cabecas,
                        self.quant_olhos,
                        self.quant_chifres,
                        self.quant_caudas,
                        self.quant_tentaculos,
                    ],
                    spacing=5,
                    top= 434,
                    left= 980,
                ),
                ft.Container(
                    top=815,
                    left=830,

                    content= ft.Row(
                        controls= [
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x,on_click=self.pesquisar_especie,)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.especie.value = ''
        self.especie.update()

        self.cor.value = None
        self.cor.update()

        self.quant_braco.value = ''
        self.quant_braco.update()

        self.quant_maos.value = ''
        self.quant_maos.update()

        self.quant_pernas.value = ''
        self.quant_pernas.update()        

        self.quant_pes.value = ''
        self.quant_pes.update()

        self.quant_cabecas.value = ''
        self.quant_cabecas.update()

        self.quant_olhos.value = ''
        self.quant_olhos.update()

        self.quant_chifres.value = ''
        self.quant_chifres.update()

        self.quant_caudas.value = ''
        self.quant_caudas.update()

        self.quant_tentaculos.value = ''
        self.quant_tentaculos.update()

    # Método para validar
    def validacao(self, e):
        self.submeter()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                cur.execute(
                    """
                    DELETE FROM Aparencia
                    WHERE Especie = ?
                    """,
                    (
                        self.especie.value,
                    ),
                )
                con.commit()
                # Limpar os campos após a eliminação
                self.limpar(None)

                self.ad1.content.value = 'Dados Eliminados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

        except Exception as ex:
            self.ad1.content.value = 'Erro desconhecido ao eliminar dados.'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_especie(self, e):
        especie_pesquisa = self.especie.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT CorPele, QuantBracos, QuantMaos, QuantPernas, QuantPes, QuantCabecas, QuantOlhos, QuantChifres, QuantCaudas, QuantTentaculos
                    FROM Aparencia
                    WHERE Especie = ?
                    """,
                    (especie_pesquisa,),
                )
                result = cur.fetchone()
                if result:                    
                # Atualizar os valores dos controles com os dados da pesquisa
                    self.cor.value = result[0]
                    self.quant_braco.value = result[1]
                    self.quant_maos.value = result[2]
                    self.quant_pernas.value = result[3]
                    self.quant_pes.value = result[4]
                    self.quant_cabecas.value = result[5]
                    self.quant_olhos.value = result[6]
                    self.quant_chifres.value = result[7]
                    self.quant_caudas.value = result[8]
                    self.quant_tentaculos.value = result[9]
                    self.page.update()
                else:
                    self.page.dialog = self.ad2
                    self.ad2.open = True
                    self.page.update()           
        except:
            pass
    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaIdentApa
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentApa(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class ListarAparencia: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.page.auto_scroll=True
        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)

        self.listar = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Espécie")),
                ft.DataColumn(ft.Text("Cor da Pele")),
                ft.DataColumn(ft.Text("Braços")),
                ft.DataColumn(ft.Text("Mãos")),
                ft.DataColumn(ft.Text("Pernas")),
                ft.DataColumn(ft.Text("Pés")),
                ft.DataColumn(ft.Text("Cabeças")),
                ft.DataColumn(ft.Text("Olhos")),
                ft.DataColumn(ft.Text("Chifres")),
                ft.DataColumn(ft.Text("Caudas")),
                ft.DataColumn(ft.Text("Tentáculos")),
            ],
            rows=[],  # Inicialmente vazia, os dados serão preenchidos posteriormente
        )
        self.preencher_tabela()

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        self.btn_voltar,
                        self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=400,
                    content=self.listar,  # Adicionando a DataTable à página
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para preencher a DataTable com os dados do banco de dados
    def preencher_tabela(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT Especie, CorPele, QuantBracos, QuantMaos, QuantPernas, QuantPes, QuantCabecas, QuantOlhos, QuantChifres, QuantCaudas, QuantTentaculos
                    FROM Aparencia
                    """
                )
                data = cur.fetchall()
                # Limpar qualquer dado anterior
                self.listar.rows.clear()
                # Preencher a tabela com os novos dados
                for row in data:
                    self.listar.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]))
        except sqlite3.Error as e:
            print("Erro ao recuperar dados da tabela Modelo:", e)

    # Ligação para o Menu Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaIdentApa
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentApa(self.page)
        voltar.main_page()

    def main_page(self):
        pass

class InserirIdentificacao: #Funcional
    def __init__(self, page:ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color = {
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor = {
                ft.MaterialState.HOVERED:ft.colors.CYAN,
                ft.MaterialState.DEFAULT:ft.colors.AMBER,
            },
            padding = {
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text= 'Voltar', icon = ft.icons.ARROW_BACK_ROUNDED , style = x, on_click= self.voltar)
        btn_menu   = ft.ElevatedButton(text='Menu',icon=ft.icons.MENU, style = x, on_click= self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style= x, on_click = self.limpar)
        btn_submit = ft.ElevatedButton(text='Inserir', style= x, on_click= self.validacao)
        btn_fechar = ft.TextButton(text = 'Fechar', on_click = self.pop)
        btn_nascimento = ft.ElevatedButton(text='Data de nascimento', width=140, height=70, style= x, on_click=lambda _: self.data_nascimento.pick_date())
        btn_vencimento_carta = ft.ElevatedButton(text='Vencimento da carta', width=140, height=70, style= x, on_click=lambda _: self.validade_carta.pick_date())
        
        # Pop Up
        self.ad1 = ft.AlertDialog(
            title= ft.Text(value = 'Alerta'),
            content = ft.Text(value = 'Preencher e/ou selecionar o(s) campo(s):\n'),
            actions = [ btn_fechar
            ],
            modal=True,
            )
        
        # Formulário
        last_ser_id = self.get_last_ser_id() 
        self.id_ser = ft.TextField(
            label = 'ID Ser',
            value= str(last_ser_id + 1),
            height=60,
            width=310,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            read_only=True,
        )

        self.nome = ft.TextField(
            label='Inserir nome',
            hint_text='Ex: Mika',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        
        self.data_nascimento = ft.DatePicker(
            cancel_text= 'Cancelar',
            confirm_text= 'Confirmar',
            error_format_text= 'Data inválida, MM/DD/YYYY',
            help_text='Data de nascimento',
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            value=''
        )
        self.planeta = ft.TextField(
            label='Inserir planeta',
            hint_text='Ex: Terra',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=50,
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        self.carta_conducao = ft.TextField(
            label='Carta de condução',
            hint_text='Ex: CDMOS',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        self.validade_carta = ft.DatePicker(
            cancel_text= 'Cancelar',
            confirm_text= 'Confirmar',
            error_format_text= 'Data inválida, MM/DD/YYYY',
            help_text='Vencimento carta',
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            value=''
        )
        self.conducao_planetaria = ft.Dropdown(
            label = 'Tipo da condução ',
            options = [
                ft.dropdown.Option(key = 'Planeta local', text = 'Planeta local'),
                ft.dropdown.Option(key = 'Entre planetas', text = 'Entre planetas'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            width=140, height=70,
            value='',
        )
        self.especie = ft.TextField(
            label = 'Espécie',
            hint_text = 'Exemplo: Humano',
            width=310, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            input_filter= ft.TextOnlyInputFilter(),
        )
        
        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Container(
                    top= 350,
                    left= 810,
            
                    content = ft.Column(
                    controls = [
                        self.id_ser,
                        self.nome,
                        btn_nascimento,
                        self.planeta,
                        self.especie,
                         
                    ],
                    spacing=15,
                )),  
                 ft.Container(
                    top= 425,
                    left= 980,
            
                    content = ft.Column(
                    controls = [
                        self.carta_conducao,
                        btn_vencimento_carta,
                        self.conducao_planetaria,
                        
                    ],
                    spacing=15,
                )),  
                ft.Container(
                    top=750,
                    left=810,

                    content= ft.Row(
                        controls= [
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),   
            ],
            expand = True,      
        )
        self.page.overlay.append(self.data_nascimento)
        self.page.overlay.append(self.validade_carta)
        self.page.add(st)     
        self.main_page()

    # Método para pegar o último ID_nave
    def get_last_ser_id(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('SELECT MAX(IDSer) FROM Identificacao')
            last_id = cur.fetchone()[0]
            return last_id if last_id else 0  # Retorna 0 se não houver nenhum ID de nave ainda  
 
    # Método para limpar
    def limpar(self, e):
        self.nome.value = ''
        self.nome.update()

        self.data_nascimento.value = ''
        self.data_nascimento.update()

        self.planeta.value = ''
        self.planeta.update()

        self.carta_conducao.value = ''
        self.carta_conducao.update()

        self.validade_carta.value = ''
        self.validade_carta.update()

        self.conducao_planetaria.value = ''
        self.conducao_planetaria.update()

        self.especie.value = ''
        self.especie.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.nome.value == '':
            campos_em_branco.append('Nome')

        if self.data_nascimento.value == None:
            campos_em_branco.append('Data de nascimento')

        if self.planeta.value == '':
            campos_em_branco.append('Planeta')

        if self.carta_conducao.value == '':
            campos_em_branco.append('Carta de condução')
        elif len(self.carta_conducao.value) < 5:  # Verifica se o comprimento é menor que 5
            campos_em_branco.append('Carta de condução (mínimo 5 caracteres)')

        if self.validade_carta.value == None:
            campos_em_branco.append('Vencimento da carta')

        if self.conducao_planetaria.value == '':
            campos_em_branco.append('Tipo de condução')   

        if self.especie.value == '':
            campos_em_branco.append('Espécie')            

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco ou inválidos:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
            # Verificar se a Espécie existe na tabela Aparencia
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            try:
                cur.execute("SELECT COUNT(*) FROM Aparencia WHERE Especie = ?", (self.especie.value,))
                count = cur.fetchone()[0]

                if count == 0:
                    # Se a espécie não existir na tabela Aparencia, exibir uma mensagem de erro
                    self.ad1.content.value = "A espécie não existe"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
                    return
                else:
                    self.submeter()
            except:
                pass
            finally:
                con.close()


    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()

    # Método para salvar
    def submeter(self):

        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO Identificacao (Nome, DataNascimento, Planeta, CartaDeConducao, ValidadeCarta, ConducaoPlanetaria, Especie) VALUES (?, ?, ?, ?, ?, ?, ?)',
                             (self.nome.value, self.data_nascimento.value.strftime('%Y-%m-%d'), self.planeta.value,
                 self.carta_conducao.value, self.validade_carta.value.strftime('%Y-%m-%d'),
                 self.conducao_planetaria.value, self.especie.value))
                # Commit para salvar as alterações
                con.commit()

                # Atualizar o id_nave após a inserção4
                self.id_ser.value = str(self.get_last_ser_id() + 1)

                # Limpar os campos após a inserção
                self.limpar(None)

                # Mostrar mensagem de sucesso
                self.ad1.content.value = 'Dados inseridos com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao inserir dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentDoc(self.page)
        voltar.main_page()
    def main_page(self):
        pass
class AlterarIdentificacao: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click = self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Alterar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        btn_nascimento = ft.ElevatedButton(text='Data de nascimento', width=140, height=70, style= x, on_click=lambda _: self.data_nascimento.pick_date())
        btn_vencimento_carta = ft.ElevatedButton(text='Vencimento da carta', width=140, height=70, style= x, on_click=lambda _: self.validade_carta.pick_date())

        # Pop Up 
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_ser = ft.TextField(
            label = 'ID Ser',
            height=60,
            width=310,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )

        self.nome = ft.TextField(
            label='Inserir nome',
            hint_text='Ex: Mika',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        
        self.data_nascimento = ft.DatePicker(
            cancel_text= 'Cancelar',
            confirm_text= 'Confirmar',
            error_format_text= 'Data inválida, MM/DD/YYYY',
            help_text='Data de nascimento',
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            value='',
            disabled=True,
        )
        self.planeta = ft.TextField(
            label='Inserir planeta',
            hint_text='Ex: Terra',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=50,
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.carta_conducao = ft.TextField(
            label='Carta de condução',
            hint_text='Ex: CDMOS',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.validade_carta = ft.DatePicker(
            cancel_text= 'Cancelar',
            confirm_text= 'Confirmar',
            error_format_text= 'Data inválida, MM/DD/YYYY',
            help_text='Vencimento carta',
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            value='',
            disabled=True,
        )
        self.conducao_planetaria = ft.Dropdown(
            label = 'Tipo da condução ',
            options = [
                ft.dropdown.Option(key = 'Planeta local', text = 'Planeta local'),
                ft.dropdown.Option(key = 'Entre planetas', text = 'Entre planetas'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            width=140, height=70,
            value='',
            disabled=True,
        )
        self.especie = ft.TextField(
            label = 'Espécie',
            hint_text = 'Exemplo: Humano',
            width=310, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            input_filter= ft.TextOnlyInputFilter(),
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Container(
                    top= 350,
                    left= 810,
            
                    content = ft.Column(
                    controls = [
                        self.id_ser,
                        self.nome,
                        btn_nascimento,
                        self.planeta,
                        self.especie,
                         
                    ],
                    spacing=15,
                )),  
                 ft.Container(
                    top= 425,
                    left= 980,
            
                    content = ft.Column(
                    controls = [
                        self.carta_conducao,
                        btn_vencimento_carta,
                        self.conducao_planetaria,
                        
                    ],
                    spacing=15,
                )),  
                ft.Container(
                    top=750,
                    left=810,

                    content= ft.Row(
                        controls= [
                            btn_limpar,
                            btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x, on_click= self.pesquisar_ser)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.overlay.append(self.data_nascimento)
        self.page.overlay.append(self.validade_carta)
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.id_ser.value = ''
        self.id_ser.update()

        self.nome.value = ''
        self.nome.read_only=True
        self.nome.update()

        self.data_nascimento.value = ''
        self.data_nascimento.disabled=True
        self.data_nascimento.update()

        self.planeta.value = ''
        self.planeta.read_only=True
        self.planeta.update()

        self.carta_conducao.value = ''
        self.carta_conducao.read_only=True
        self.carta_conducao.update()

        self.validade_carta.value = ''
        self.validade_carta.disabled=True
        self.validade_carta.update()

        self.conducao_planetaria.value = ''
        self.conducao_planetaria.disabled=True
        self.conducao_planetaria.update()

        self.especie.value = ''
        self.especie.read_only=True
        self.especie.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.nome.value == '':
            campos_em_branco.append('Nome')

        if self.data_nascimento.value == None:
            campos_em_branco.append('Data de nascimento')

        if self.planeta.value == '':
            campos_em_branco.append('Planeta')

        if self.carta_conducao.value == '':
            campos_em_branco.append('Carta de condução')
        elif len(self.carta_conducao.value) < 5:  # Verifica se o comprimento é menor que 5
            campos_em_branco.append('Carta de condução (mínimo 5 caracteres)')

        if self.validade_carta.value == None:
            campos_em_branco.append('Vencimento da carta')

        if self.conducao_planetaria.value == '':
            campos_em_branco.append('Tipo de condução')   

        if self.especie.value == '':
            campos_em_branco.append('Espécie')            

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco ou inválidos:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
            # Verificar se a Espécie existe na tabela Aparencia
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            try:
                cur.execute("SELECT COUNT(*) FROM Aparencia WHERE Especie = ?", (self.especie.value,))
                count = cur.fetchone()[0]

                if count == 0:
                    # Se a espécie não existir na tabela Aparencia, exibir uma mensagem de erro
                    self.ad1.content.value = "A espécie não existe"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
                    return
                else:
                    self.submeter()
            except:
                pass
            finally:
                con.close()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE Identificacao
                    SET Nome=?, DataNascimento=?, Planeta=?, CartaDeConducao=?, ValidadeCarta=?, ConducaoPlanetaria=?, Especie=?
                    WHERE IDSer = ?
                    """,
                    (self.nome.value, self.data_nascimento.value.strftime('%Y-%m-%d'), self.planeta.value,
                 self.carta_conducao.value, self.validade_carta.value.strftime('%Y-%m-%d'),
                 self.conducao_planetaria.value, self.especie.value
                 , self.id_ser.value
                    ),
                )
                con.commit()
                # Limpar os campos após a inserção
                self.limpar(None)

                self.ad1.content.value = 'Dados alterados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao alterar dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_ser(self, e):
        id_ser_pesquisa = self.id_ser.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT Nome, DataNascimento, Planeta, CartaDeConducao, ValidadeCarta, ConducaoPlanetaria, Especie
                    FROM Identificacao
                    WHERE IDSer = ?
                    """,
                    (id_ser_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    # Preenche os campos com os valores recuperados do banco de dados
                    self.nome.value = result[0]
                    self.nome.read_only=False

                    self.data_nascimento.value = datetime.datetime.strptime(result[1], '%Y-%m-%d').date()
                    self.data_nascimento.disabled=False

                    self.planeta.value = result[2]
                    self.planeta.read_only=False

                    self.carta_conducao.value = result[3]
                    self.carta_conducao.read_only=False

                    self.validade_carta.value = datetime.datetime.strptime(result[4], '%Y-%m-%d').date()
                    self.validade_carta.disabled=False

                    self.conducao_planetaria.value = result[5]
                    self.conducao_planetaria.disabled=False

                    self.especie.value = result[6]
                    self.especie.read_only=False
                    # Atualiza os campos na interface do usuário
                    self.nome.update()
                    self.data_nascimento.update()
                    self.planeta.update()
                    self.carta_conducao.update()
                    self.validade_carta.update()
                    self.conducao_planetaria.update()
                    self.especie.update()
                else:
                    # Se nenhum resultado for encontrado, limpa os campos
                    self.limpar(None)
                    # Exibe uma mensagem informando que o ID do SER não foi encontrado
                    self.ad1.content.value = "ID do SER não encontrado"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
        except:
            pass

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentDoc(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class EliminarIdentificacao: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        btn_submit = ft.ElevatedButton(text='Eliminar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        btn_nascimento = ft.ElevatedButton(text='Data de nascimento', width=140, height=70, style= x, on_click=lambda _: self.data_nascimento.pick_date())
        btn_vencimento_carta = ft.ElevatedButton(text='Vencimento da carta', width=140, height=70, style= x, on_click=lambda _: self.validade_carta.pick_date())

        # Pop Up 
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_ser = ft.TextField(
            label = 'ID Ser',
            height=60,
            width=310,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )

        self.nome = ft.TextField(
            label='Inserir nome',
            hint_text='Ex: Mika',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=25,
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        
        self.data_nascimento = ft.TextField(
            label='Data de nascimento',
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.planeta = ft.TextField(
            label='Inserir planeta',
            hint_text='Ex: Terra',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=50,
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.carta_conducao = ft.TextField(
            label='Carta de condução',
            hint_text='Ex: CDMOS',
            input_filter=ft.TextOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.validade_carta = ft.TextField(
            label='Vencimento carta',
            width=120, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.conducao_planetaria = ft.Dropdown(
            label = 'Tipo da condução ',
            options = [
                ft.dropdown.Option(key = 'Planeta local', text = 'Planeta local'),
                ft.dropdown.Option(key = 'Entre planetas', text = 'Entre planetas'),
            ],
            filled=True,
            bgcolor = ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            width=140, height=70,
            value='',
            disabled=True,
        )
        self.especie = ft.TextField(
            label = 'Espécie',
            hint_text = 'Exemplo: Humano',
            width=310, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            input_filter= ft.TextOnlyInputFilter(),
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),
                ft.Container(
                    top= 350,
                    left= 810,
            
                    content = ft.Column(
                    controls = [
                        self.id_ser,
                        self.nome,
                        self.data_nascimento,
                        self.planeta,
                        self.especie,
                         
                    ],
                    spacing=15,
                )),  
                 ft.Container(
                    top= 425,
                    left= 980,
            
                    content = ft.Column(
                    controls = [
                        self.carta_conducao,
                        self.validade_carta,
                        self.conducao_planetaria,
                        
                    ],
                    spacing=15,
                )),  
                ft.Container(
                    top=750,
                    left=810,

                    content= ft.Row(
                        controls= [
                        btn_limpar,
                        btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing= 95,
                    )
                ),             
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x, on_click= self.pesquisar_ser)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()
    
    # Método para limpar
    def limpar(self, e):
        self.id_ser.value = ''
        self.id_ser.update()

        self.nome.value = ''
        self.nome.update()

        self.data_nascimento.value = ''
        self.data_nascimento.update()

        self.planeta.value = ''
        self.planeta.update()

        self.carta_conducao.value = ''
        self.carta_conducao.update()

        self.validade_carta.value = ''
        self.validade_carta.update()

        self.conducao_planetaria.value = ''
        self.conducao_planetaria.update()

        self.especie.value = ''
        self.especie.update()

    # Método para validar
    def validacao(self, e):
        self.submeter()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
        
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                """
                DELETE FROM Identificacao
                WHERE IDSer = ?
                """,
                ( self.id_ser.value,),)
                con.commit()
                # Limpar os campos após a eliminação
                self.limpar(None)

                self.ad1.content.value = 'Dados Eliminados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

        except Exception as ex:
            self.ad1.content.value = 'Erro desconhecido ao eliminar dados.'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_ser(self, e):
        id_ser_pesquisa = self.id_ser.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT Nome, DataNascimento, Planeta, CartaDeConducao, ValidadeCarta, ConducaoPlanetaria, Especie
                    FROM Identificacao
                    WHERE IDSer = ?
                    """,
                    (id_ser_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    # Preenche os campos com os valores recuperados do banco de dados
                    self.nome.value = result[0]
                    self.data_nascimento.value = result[1]
                    self.planeta.value = result[2]
                    self.carta_conducao.value = result[3]
                    self.validade_carta.value = result[4]
                    self.conducao_planetaria.value = result[5]
                    self.especie.value = result[6]
                    # Atualiza os campos na interface do usuário
                    self.nome.update()
                    self.data_nascimento.update()
                    self.planeta.update()
                    self.carta_conducao.update()
                    self.validade_carta.update()
                    self.conducao_planetaria.update()
                    self.especie.update()
                else:
                    # Se nenhum resultado for encontrado, limpa os campos
                    self.limpar(None)
                    # Exibe uma mensagem informando que o ID do SER não foi encontrado
                    self.ad1.content.value = "ID do SER não encontrado"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
        except:
            pass

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentDoc(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class ListarIdentificacao: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.page.auto_scroll=True
        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)

        self.listar = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Ser")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Data de Nascimento")),
                ft.DataColumn(ft.Text("Planeta")),
                ft.DataColumn(ft.Text("Carta de Condução")),
                ft.DataColumn(ft.Text("Validade da Carta")),
                ft.DataColumn(ft.Text("Tipo da Condução")),
                ft.DataColumn(ft.Text("Espécie")),
            ],
            rows=[],  # Inicialmente vazia, os dados serão preenchidos posteriormente
        )
        self.preencher_tabela()

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        self.btn_voltar,
                        self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=450,
                    content=self.listar,  # Adicionando a DataTable à página
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para preencher a DataTable com os dados do banco de dados
    def preencher_tabela(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT IDSer, Nome, DataNascimento, Planeta, CartaDeConducao, ValidadeCarta, ConducaoPlanetaria, Especie
                    FROM Identificacao
                    """
                )
                data = cur.fetchall()
                # Limpar qualquer dado anterior
                self.listar.rows.clear()
                # Preencher a tabela com os novos dados
                for row in data:
                    self.listar.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]))
        except sqlite3.Error as e:
            print("Erro ao recuperar dados da tabela Modelo:", e)

    # Ligação para o Menu Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaIdentDoc(self.page)
        voltar.main_page()

    def main_page(self):
        pass

class InserirInfracao: #Funcional
 
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color = {
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor = {
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding = {
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        self.btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        self.btn_submit = ft.ElevatedButton(text='Inserir', style=x, on_click=self.validacao)
        self.btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        self.btn_vencimento = ft.ElevatedButton(text='Vencimento da infração', height=60, width=310, style=x, on_click=lambda _: self.vencimento_infracao.pick_date())

        # Pop Up
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[self.btn_fechar],
            modal=True,
        )

        # Formulário
        last_id_infracao = self.get_last_infracao_id() 
        self.id_infracao = ft.TextField(
            label='ID Infração',
            value=str(last_id_infracao + 1),
            height=60,
            width=310,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            read_only=True,
        )
        self.valor = ft.TextField(
            label='Valor da infração',
            hint_text='Ex: 1000',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=25,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        self.vencimento_infracao = ft.DatePicker(
            cancel_text='Cancelar',
            confirm_text='Confirmar',
            error_format_text='Data inválida, MM/DD/YYYY',
            help_text='Vencimento da infração',
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            value='',
        )
        self.descricao = ft.TextField(
            label='Descrição',
            hint_text='Ex: Nave roubada',
            max_length=200,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        self.id_ser = ft.TextField(
            label='ID Ser',
            hint_text='Ex: 1',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )
        self.id_nave = ft.TextField(
            label='ID Nave',
            hint_text='Ex: 1',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
        )

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png', 
                    image_fit=ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=ft.Column(
                        controls=[
                            self.id_infracao,
                            self.valor,
                            self.descricao,
                            self.btn_vencimento,
                        ],
                        spacing=15,
                    )
                ),  
                ft.Container(
                    top=425,
                    left=980,
                    content=ft.Column(
                        controls=[
                            self.id_ser,
                            self.id_nave,
                        ],
                        spacing=15,
                    )
                ),  
                ft.Container(
                    top=750,
                    left=810,
                    content=ft.Row(
                        controls=[
                            self.btn_limpar,
                            self.btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=95,
                    )
                ),             
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                        controls=[
                            self.btn_voltar,
                            self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
            ],
            expand=True,      
        )
        self.page.overlay.append(self.vencimento_infracao)
        self.page.add(st)

    # Método para pegar o último
    def get_last_infracao_id(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('SELECT MAX(IDInfracao) FROM Infracao')
                last_id_infracao = cur.fetchone()[0]
                return last_id_infracao if last_id_infracao else 0
        except sqlite3.Error as e:
            print(f'Erro ao acessar o banco de dados: {e}')
            return 0

    # Método para limpar
    def limpar(self, e):
        self.valor.value = ''
        self.valor.update()

        self.descricao.value = ''
        self.descricao.update()

        self.id_ser.value = ''
        self.id_ser.update()

        self.id_nave.value = ''
        self.id_nave.update()

        self.vencimento_infracao.value = ''
        self.vencimento_infracao.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.valor.value == '':
            campos_em_branco.append('Valor da infração')

        if self.vencimento_infracao.value == None:
            campos_em_branco.append('Vencimento da infração')

        if self.descricao.value == '':
            campos_em_branco.append('Descrição')

        if self.id_ser.value == '' and self.id_nave.value == '':
            campos_em_branco.append('Preencha ao menos um dos campos: ID Ser, ID Nave')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco ou inválidos:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
            try:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    if self.id_ser.value:
                        cur.execute("SELECT COUNT(*) FROM Identificacao WHERE IDSer = ?", (self.id_ser.value,))
                        count = cur.fetchone()[0]
                        if count == 0:
                            self.ad1.content.value = "O ID ser não existe"
                            self.page.dialog = self.ad1
                            self.ad1.open = True
                            self.page.update()
                            return
                    if self.id_nave.value:
                        cur.execute("SELECT COUNT(*) FROM Nave WHERE IDNave = ?", (self.id_nave.value,))
                        count = cur.fetchone()[0]
                        if count == 0:
                            self.ad1.content.value = "O ID nave não existe"
                            self.page.dialog = self.ad1
                            self.ad1.open = True
                            self.page.update()
                            return
                    self.submeter()
            except sqlite3.Error as ex:
                self.ad1.content.value = f'Erro ao acessar o banco de dados: {str(ex)}'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
            
    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()

    # Método para salvar    
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO Infracao (Valor, Vencimento, Descricao, IDSer, IDNave) VALUES (?, ?, ?, ?, ?)',
                             (self.valor.value, self.vencimento_infracao.value.strftime('%Y-%m-%d'), self.descricao.value, self.id_ser.value, self.id_nave.value))
                con.commit()
                self.id_infracao.value = str(self.get_last_infracao_id() + 1)
                self.limpar(None)
                self.ad1.content.value = 'Dados inseridos com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            self.ad1.content.value = f'Erro ao inserir dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
    
    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()
        
    # Ligação para GuiaInfra
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaInfra(self.page)
        voltar.main_page()

    def main_page(self):
        pass
class AlterarInfracao: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        self.btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        self.btn_submit = ft.ElevatedButton(text='Alterar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        self.btn_vencimento = ft.ElevatedButton(text='Vencimento da infração', height=60, width=310, style=x, on_click=lambda _: self.vencimento_infracao.pick_date())

        # Pop Up 
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_infracao = ft.TextField(
            label='ID Infração',
            height=60,
            width=310,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        self.valor = ft.TextField(
            label='Valor da infração',
            hint_text='Ex: 1000',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=25,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.vencimento_infracao = ft.DatePicker(
            cancel_text='Cancelar',
            confirm_text='Confirmar',
            error_format_text='Data inválida, MM/DD/YYYY',
            help_text='Vencimento da infração',
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            value='',
            disabled=True,
        )
        self.descricao = ft.TextField(
            label='Descrição',
            hint_text='Ex: Nave roubada',
            max_length=200,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
            
        )
        self.id_ser = ft.TextField(
            label='ID Ser',
            hint_text='Ex: 1',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.id_nave = ft.TextField(
            label='ID Nave',
            hint_text='Ex: 1',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png', 
                    image_fit=ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=ft.Column(
                        controls=[
                            self.id_infracao,
                            self.valor,
                            self.descricao,
                            self.btn_vencimento,
                        ],
                        spacing=15,
                    )
                ),  
                ft.Container(
                    top=425,
                    left=980,
                    content=ft.Column(
                        controls=[
                            self.id_ser,
                            self.id_nave,
                        ],
                        spacing=15,
                    )
                ),  
                ft.Container(
                    top=750,
                    left=810,
                    content=ft.Row(
                        controls=[
                            self.btn_limpar,
                            self.btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=95,
                    )
                ),             
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                        controls=[
                            self.btn_voltar,
                            self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                 ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x, on_click= self.pesquisar_infra)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,      
        )
        self.page.overlay.append(self.vencimento_infracao)
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.id_infracao.value = ''
        self.id_infracao.update()

        self.valor.value = ''
        self.valor.read_only=True
        self.valor.update()

        self.descricao.value = ''
        self.descricao.read_only=True
        self.descricao.update()

        self.id_ser.value = ''
        self.id_ser.read_only=True
        self.id_ser.update()

        self.id_nave.value = ''
        self.id_nave.read_only=True
        self.id_nave.update()

        self.vencimento_infracao.value = ''
        self.vencimento_infracao.disabled=True
        self.vencimento_infracao.update()

    # Método para validar
    def validacao(self, e):
        campos_em_branco = []

        if self.valor.value == '':
            campos_em_branco.append('Valor da infração')

        if self.vencimento_infracao.value == None:
            campos_em_branco.append('Vencimento da infração')

        if self.descricao.value == '':
            campos_em_branco.append('Descrição')

        if self.id_ser.value == '' and self.id_nave.value == '':
            campos_em_branco.append('Preencha ao menos um dos campos: ID Ser, ID Nave')

        if campos_em_branco:
            mensagem = 'Os seguintes campos estão em branco ou inválidos:'
            for campo in campos_em_branco:
                mensagem += f'\n- {campo}'
            self.ad1.content.value = mensagem
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()
        else:
            try:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    if self.id_ser.value:
                        cur.execute("SELECT COUNT(*) FROM Identificacao WHERE IDSer = ?", (self.id_ser.value,))
                        count = cur.fetchone()[0]
                        if count == 0:
                            self.ad1.content.value = "O ID ser não existe"
                            self.page.dialog = self.ad1
                            self.ad1.open = True
                            self.page.update()
                            return
                    if self.id_nave.value:
                        cur.execute("SELECT COUNT(*) FROM Nave WHERE IDNave = ?", (self.id_nave.value,))
                        count = cur.fetchone()[0]
                        if count == 0:
                            self.ad1.content.value = "O ID nave não existe"
                            self.page.dialog = self.ad1
                            self.ad1.open = True
                            self.page.update()
                            return
                    self.submeter()
            except sqlite3.Error as ex:
                self.ad1.content.value = f'Erro ao acessar o banco de dados: {str(ex)}'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
    
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE Infracao
                    SET Valor=?, Vencimento=?, Descricao=?, IDSer=?, IDNave=?
                    WHERE IDInfracao = ?
                    """,
                     (self.valor.value, self.vencimento_infracao.value.strftime('%Y-%m-%d'), self.descricao.value,self.id_ser.value, self.id_nave.value, self.id_infracao.value),)
                con.commit()
                # Limpar os campos após a inserção
                self.limpar(None)

                self.ad1.content.value = 'Dados alterados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()
        except sqlite3.Error as e:
            # Se houver algum erro ao inserir os dados, mostrar mensagem de erro
            self.ad1.content.value = f'Erro ao alterar dados: {str(e)}'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_infra(self, e):
        id_infra_pesquisa = self.id_infracao.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT Valor, Vencimento, Descricao, IDSer, IDNave
                    FROM Infracao
                    WHERE IDInfracao = ?
                    """,
                    (id_infra_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    # Preenche os campos com os valores recuperados do banco de dados
                    self.valor.value = result[0]
                    self.valor.read_only=False

                    self.vencimento_infracao.value = datetime.datetime.strptime(result[1], '%Y-%m-%d').date()
                    self.vencimento_infracao.disabled = False

                    self.descricao.value = result[2]
                    self.descricao.read_only = False

                    self.id_ser.value = result[3]
                    self.id_ser.read_only = False

                    self.id_nave.value = result[4]
                    self.id_nave.read_only = False

                    # Atualiza os campos na interface do usuário
                    self.valor.update()
                    self.vencimento_infracao.update()
                    self.descricao.update()
                    self.id_ser.update()
                    self.id_nave.update()
                else:
                    # Se nenhum resultado for encontrado, limpa os campos
                    self.limpar(None)
                    # Exibe uma mensagem informando que o ID do SER não foi encontrado
                    self.ad1.content.value = "ID infração não encontrado"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
        except Exception as ex:
            print("Ocorreu um erro durante a pesquisa:", ex)

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaInfra(self.page)
        voltar.main_page()
    def main_page(self):
        pass
class EliminarInfracao: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        self.btn_limpar = ft.ElevatedButton(text='Limpar', style=x, on_click=self.limpar)
        self.btn_submit = ft.ElevatedButton(text='Eliminar', style=x, on_click=self.validacao)
        btn_fechar = ft.TextButton(text='Fechar', on_click=self.pop)
        btn_fechar2 = ft.TextButton(text='Fechar', on_click=self.pop2)
        self.btn_vencimento = ft.ElevatedButton(text='Vencimento da infração', height=60, width=310, style=x, on_click=lambda _: self.vencimento_infracao.pick_date())

        # Pop Up 
        self.ad1 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Preencher e/ou selecionar o(s) campo(s):\n'),
            actions=[btn_fechar],
            modal=True,
        )
        self.ad2 = ft.AlertDialog(
            title=ft.Text(value='Alerta'),
            content=ft.Text(value='Não encontrado!\n'),
            actions=[btn_fechar2],
            modal=True,
        )

        # Formulário
        self.id_infracao = ft.TextField(
            label='ID Infração',
            height=60,
            width=310,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
        )
        self.valor = ft.TextField(
            label='Valor da infração',
            hint_text='Ex: 1000',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=25,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.vencimento_infracao = ft.DatePicker(
            cancel_text='Cancelar',
            confirm_text='Confirmar',
            error_format_text='Data inválida, MM/DD/YYYY',
            help_text='Vencimento da infração',
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            value='',
            disabled=True,
        )
        self.descricao = ft.TextField(
            label='Descrição',
            hint_text='Ex: Nave roubada',
            max_length=200,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
            
        )
        self.id_ser = ft.TextField(
            label='ID Ser',
            hint_text='Ex: 1',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )
        self.id_nave = ft.TextField(
            label='ID Nave',
            hint_text='Ex: 1',
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=5,
            width=140, height=70,
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(50),
            value='',
            read_only=True,
        )

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png', 
                    image_fit=ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=350,
                    left=810,
                    content=ft.Column(
                        controls=[
                            self.id_infracao,
                            self.valor,
                            self.descricao,
                            self.btn_vencimento,
                        ],
                        spacing=15,
                    )
                ),  
                ft.Container(
                    top=425,
                    left=980,
                    content=ft.Column(
                        controls=[
                            self.id_ser,
                            self.id_nave,
                        ],
                        spacing=15,
                    )
                ),  
                ft.Container(
                    top=750,
                    left=810,
                    content=ft.Row(
                        controls=[
                            self.btn_limpar,
                            self.btn_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=95,
                    )
                ),             
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                        controls=[
                            self.btn_voltar,
                            self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                 ft.Container(
                    top=350,
                    left=1120,
                    content=ft.Column(
                    controls=[    
                        ft.ElevatedButton(text='Pesquisar',style=x, on_click= self.pesquisar_infra)
                        ],
                        spacing=15,
                    ),
                ),
            ],
            expand=True,      
        )
        self.page.overlay.append(self.vencimento_infracao)
        self.page.add(st)
        self.main_page()

    # Método para limpar
    def limpar(self, e):
        self.id_infracao.value = ''
        self.id_infracao.update()

        self.valor.value = ''
        self.valor.read_only=True
        self.valor.update()

        self.descricao.value = ''
        self.descricao.read_only=True
        self.descricao.update()

        self.id_ser.value = ''
        self.id_ser.read_only=True
        self.id_ser.update()

        self.id_nave.value = ''
        self.id_nave.read_only=True
        self.id_nave.update()

        self.vencimento_infracao.value = ''
        self.vencimento_infracao.disabled=True
        self.vencimento_infracao.update()

    # Método para validar
    def validacao(self, e):
        self.submeter()

    # Método para fechar o pop up
    def pop(self, e):
        self.page.dialog = self.ad1
        self.ad1.open = False
        self.page.update()
    def pop2(self, e):
        self.page.dialog = self.ad2
        self.ad2.open = False
        self.page.update()
        
    # Método para salvar 
    def submeter(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                """
                DELETE FROM Infracao
                WHERE IDInfracao = ?
                """,
                ( self.id_ser.value,),)
                con.commit()
                # Limpar os campos após a eliminação
                self.limpar(None)

                self.ad1.content.value = 'Dados Eliminados com sucesso!'
                self.page.dialog = self.ad1
                self.ad1.open = True
                self.page.update()

        except Exception as ex:
            self.ad1.content.value = 'Erro desconhecido ao eliminar dados.'
            self.page.dialog = self.ad1
            self.ad1.open = True
            self.page.update()

    def pesquisar_infra(self, e):
        id_infra_pesquisa = self.id_infracao.value
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT Valor, Vencimento, Descricao, IDSer, IDNave
                    FROM Infracao
                    WHERE IDInfracao = ?
                    """,
                    (id_infra_pesquisa,),
                )
                result = cur.fetchone()
                if result:
                    # Preenche os campos com os valores recuperados do banco de dados
                    self.valor.value = result[0]
                    self.vencimento_infracao.value = datetime.datetime.strptime(result[1], '%Y-%m-%d').date()
                    self.descricao.value = result[2]
                    self.id_ser.value = result[3]
                    self.id_nave.value = result[4]

                    # Atualiza os campos na interface do usuário
                    self.valor.update()
                    self.vencimento_infracao.update()
                    self.descricao.update()
                    self.id_ser.update()
                    self.id_nave.update()
                else:
                    # Se nenhum resultado for encontrado, limpa os campos
                    self.limpar(None)
                    # Exibe uma mensagem informando que o ID do SER não foi encontrado
                    self.ad1.content.value = "ID infração não encontrado"
                    self.page.dialog = self.ad1
                    self.ad1.open = True
                    self.page.update()
        except Exception as ex:
            print("Ocorreu um erro durante a pesquisa:", ex)

    # Ligação para Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaInfra(self.page)
        voltar.main_page()
    def main_page(self):
        pass
class ListarInfracao: #Funcional
    def __init__(self, page: ft.Page):
        # Configuração da página
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.page.auto_scroll = True
        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Botões
        self.btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        self.btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)

        self.listar = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Infração")),
                ft.DataColumn(ft.Text("Valor")),
                ft.DataColumn(ft.Text("Vencimento da Infração")),
                ft.DataColumn(ft.Text("Descrição")),
                ft.DataColumn(ft.Text("ID Ser")),
                ft.DataColumn(ft.Text("ID Nave")),
            ],
            rows=[],  # Inicialmente vazia, os dados serão preenchidos posteriormente
        )
        self.preencher_tabela()

        # Componentes na página
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                    controls=[
                        self.btn_voltar,
                        self.btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=350,
                    left=600,
                    content=self.listar,  # Adicionando a DataTable à página
                ),
            ],
            expand=True,
        )
        self.page.add(st)
        self.main_page()

    # Método para preencher a DataTable com os dados do banco de dados
    def preencher_tabela(self):
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT IDInfracao, Valor, Vencimento, Descricao, IDSer, IDNave
                    FROM Infracao
                    """
                )
                data = cur.fetchall()
                # Limpar qualquer dado anterior
                self.listar.rows.clear()
                # Preencher a tabela com os novos dados
                for row in data:
                    self.listar.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]))
        except sqlite3.Error as e:
            print("Erro ao recuperar dados da tabela Modelo:", e)

    # Ligação para o Menu Principal
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para GuiaNavMod 
    def voltar(self, e):
        self.page.clean()
        voltar = GuiaInfra(self.page)
        voltar.main_page()
    def main_page(self):
        pass

class GuiaNaveMod: #Funcional
    def __init__(self, page:ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style = x, on_click = self.abrir_menu)
        btn_isnerir = ft.ElevatedButton(text='Inserir', style = x, on_click = self.inserir)
        btn_alterar = ft.ElevatedButton(text='Alterar',style = x, on_click = self.alterar)
        btn_eliminar = ft.ElevatedButton(text='Eliminar',style = x, on_click = self.eliminar)
        btn_listar = ft.ElevatedButton(text='Listar',style = x, on_click = self.listar)

        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),               
                ft.Container(
                    left = 0,
                    right = 570,
                    top = 525,

                    height = 180,
                    width = 1920,
                    image_src = 'Imagens/Inserir.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 0,
                    right = 180,
                    top = 515,

                    height = 200,
                    width = 1920,
                    image_src = 'Imagens/Alterar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ),
                ft.Container(
                    left = 200,
                    right = 0,
                    top = 480,

                    height = 270,
                    width = 1920,
                    image_src = 'Imagens/Deletar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 575,
                    right = 0,
                    top = 530,

                    height = 170,
                    width = 1920,
                    image_src = 'Imagens/Consultar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    top = 500,
                    right = 500,
                    left = 500,
                    content = ft.Row(
                    controls = [
                         btn_isnerir,
                         btn_alterar,
                         btn_eliminar,
                         btn_listar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 100,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()
        
    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Nave 
    def voltar(self, e):
        self.page.clean()
        voltar = Nave(self.page)
        voltar.main_page()

    # Ligação para Inserir dados na tabela Modelo
    def inserir(self, e):
        self.page.clean()
        inserir = InserirModelo(self.page)
        inserir.main_page()
     # Ligação para Alterar dados na tabela Modelo
    def alterar(self, e):
        self.page.clean()
        alterar = AlterarModelo(self.page)
        alterar.main_page()
    # Ligação para Eliminar dados na tabela Modelo    
    def eliminar(self, e):
        self.page.clean()
        eliminar = EliminarModelo(self.page)
        eliminar.main_page()
    
    # Ligação para Listar dados da tabela Modelo 
    def listar(self, e):
        self.page.clean()
        listar = ListarModelo(self.page)
        listar.main_page()

    def main_page(self):
        pass
class GuiaNaveDoc: #Funcional
    def __init__(self, page:ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style = x, on_click = self.abrir_menu)
        btn_isnerir = ft.ElevatedButton(text='Inserir', style = x, on_click = self.inserir)
        btn_alterar = ft.ElevatedButton(text='Alterar',style = x, on_click = self.alterar)
        btn_eliminar = ft.ElevatedButton(text='Eliminar',style = x, on_click = self.eliminar)
        btn_listar = ft.ElevatedButton(text='Listar',style = x, on_click = self.listar)

        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),               
                ft.Container(
                    left = 0,
                    right = 570,
                    top = 525,

                    height = 180,
                    width = 1920,
                    image_src = 'Imagens/Inserir.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 0,
                    right = 180,
                    top = 515,

                    height = 200,
                    width = 1920,
                    image_src = 'Imagens/Alterar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ),
                ft.Container(
                    left = 200,
                    right = 0,
                    top = 480,

                    height = 270,
                    width = 1920,
                    image_src = 'Imagens/Deletar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 575,
                    right = 0,
                    top = 530,

                    height = 170,
                    width = 1920,
                    image_src = 'Imagens/Consultar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    top = 500,
                    right = 500,
                    left = 500,
                    content = ft.Row(
                    controls = [
                         btn_isnerir,
                         btn_alterar,
                         btn_eliminar,
                         btn_listar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 100,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()
        
    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Nave 
    def voltar(self, e):
        self.page.clean()
        voltar = Nave(self.page)
        voltar.main_page()

    # Ligação para Inserir dados na tabela Nave
    def inserir(self, e):
        self.page.clean()
        inserir = InserirNave(self.page)
        inserir.main_page()
     # Ligação para Alterar dados na tabela Nave
    def alterar(self, e):
        self.page.clean()
        alterar = AlterarNave(self.page)
        alterar.main_page()
    # Ligação para Eliminar dados na tabela Nave   
    def eliminar(self, e):
        self.page.clean()
        eliminar = EliminarNave(self.page)
        eliminar.main_page()
    
    # Ligação para Listar dados da tabela Nave 
    def listar(self, e):
        self.page.clean()
        listar = ListarNave(self.page)
        listar.main_page()

    def main_page(self):
        pass
class GuiaIdentDoc: #Funcional
    def __init__(self, page:ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style = x, on_click = self.abrir_menu)
        btn_isnerir = ft.ElevatedButton(text='Inserir', style = x, on_click = self.inserir)
        btn_alterar = ft.ElevatedButton(text='Alterar',style = x, on_click = self.alterar)
        btn_eliminar = ft.ElevatedButton(text='Eliminar',style = x, on_click = self.eliminar)
        btn_listar = ft.ElevatedButton(text='Listar',style = x, on_click = self.listar)

        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),               
                ft.Container(
                    left = 0,
                    right = 570,
                    top = 525,

                    height = 180,
                    width = 1920,
                    image_src = 'Imagens/Inserir.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 0,
                    right = 180,
                    top = 515,

                    height = 200,
                    width = 1920,
                    image_src = 'Imagens/Alterar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ),
                ft.Container(
                    left = 200,
                    right = 0,
                    top = 480,

                    height = 270,
                    width = 1920,
                    image_src = 'Imagens/Deletar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 575,
                    right = 0,
                    top = 530,

                    height = 170,
                    width = 1920,
                    image_src = 'Imagens/Consultar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    top = 500,
                    right = 500,
                    left = 500,
                    content = ft.Row(
                    controls = [
                         btn_isnerir,
                         btn_alterar,
                         btn_eliminar,
                         btn_listar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 100,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()
        
    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Identificacao
    def voltar(self, e):
        self.page.clean()
        voltar = Identificacao(self.page)
        voltar.main_page()

    # Ligação para Inserir dados na tabela Identificacao
    def inserir(self, e):
        self.page.clean()
        inserir = InserirIdentificacao(self.page)
        inserir.main_page()
     # Ligação para Alterar dados na tabela Identificacao
    def alterar(self, e):
        self.page.clean()
        alterar = AlterarIdentificacao(self.page)
        alterar.main_page()
    # Ligação para Eliminar dados na tabela Identificacao  
    def eliminar(self, e):
        self.page.clean()
        eliminar = EliminarIdentificacao(self.page)
        eliminar.main_page()
    
    # Ligação para Listar dados da tabela Identificacao
    def listar(self, e):
        self.page.clean()
        listar = ListarIdentificacao(self.page)
        listar.main_page()

    def main_page(self):
        pass
class GuiaIdentApa: #Funcional
    def __init__(self, page:ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style = x, on_click = self.abrir_menu)
        btn_isnerir = ft.ElevatedButton(text='Inserir', style = x, on_click = self.inserir)
        btn_alterar = ft.ElevatedButton(text='Alterar',style = x, on_click = self.alterar)
        btn_eliminar = ft.ElevatedButton(text='Eliminar',style = x, on_click = self.eliminar)
        btn_listar = ft.ElevatedButton(text='Listar',style = x, on_click = self.listar)

        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),               
                ft.Container(
                    left = 0,
                    right = 570,
                    top = 525,

                    height = 180,
                    width = 1920,
                    image_src = 'Imagens/Inserir.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 0,
                    right = 180,
                    top = 515,

                    height = 200,
                    width = 1920,
                    image_src = 'Imagens/Alterar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ),
                ft.Container(
                    left = 200,
                    right = 0,
                    top = 480,

                    height = 270,
                    width = 1920,
                    image_src = 'Imagens/Deletar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 575,
                    right = 0,
                    top = 530,

                    height = 170,
                    width = 1920,
                    image_src = 'Imagens/Consultar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    top = 500,
                    right = 500,
                    left = 500,
                    content = ft.Row(
                    controls = [
                         btn_isnerir,
                         btn_alterar,
                         btn_eliminar,
                         btn_listar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 100,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()
        
    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Identificação 
    def voltar(self, e):
        self.page.clean()
        voltar = Identificacao(self.page)
        voltar.main_page()

    # Ligação para Inserir dados na tabela Aparencia
    def inserir(self, e):
        self.page.clean()
        inserir = InserirAparencia(self.page)
        inserir.main_page()
     # Ligação para Alterar dados na tabela Aparencia
    def alterar(self, e):
        self.page.clean()
        alterar = AlterarAparencia(self.page)
        alterar.main_page()
    # Ligação para Eliminar dados na tabela Aparencia 
    def eliminar(self, e):
        self.page.clean()
        eliminar = EliminarAparencia(self.page)
        eliminar.main_page()
    
    # Ligação para Listar dados da tabela Aparencia
    def listar(self, e):
        self.page.clean()
        listar = ListarAparencia(self.page)
        listar.main_page()

    def main_page(self):
        pass

class Identificacao: #Funcional
    def __init__(self, page:ft.Page):
        # Definição da classe Identificacao
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        
        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_documentacao2 = ft.ElevatedButton(text='Documentação', style=x, on_click=self.documentacao)
        btn_aparencia = ft.ElevatedButton(text='Aparência', style=x, on_click=self.aparencia)
        
        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),               
                ft.Container(
                    left = 445,
                    right = 0,
                    top = 440,

                    height = 300,
                    width = 1920,
                    image_src = 'Imagens/Alien Alone.png',  
                    opacity= 1,
                ),
                ft.Container(
                    left = 0,
                    right = 430,
                    top = 525,

                    height = 180,
                    width = 1920,
                    image_src = 'Imagens/Identificacao.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    top = 500,
                    right = 500,
                    left = 500,
                    content = ft.Row(
                    controls = [
                        btn_documentacao2,
                        btn_aparencia,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 300,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()

    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Menu 
    def voltar(self, e):
        self.page.clean()
        voltar = Principal(self.page)
        voltar.main_page()

    # Ligação para GuiaIdentDoc
    def documentacao(self, e):
        self.page.clean()
        documentacao = GuiaIdentDoc(self.page)
        documentacao.main_page()

    # Ligação para GuiaIdentApa
    def aparencia(self, e):
        self.page.clean()
        aparencia = GuiaIdentApa(self.page)
        aparencia.main_page()

    

    def main_page(self):
        pass
class GuiaInfra: #Funcional
    def __init__(self, page:ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style = x, on_click = self.abrir_menu)
        btn_isnerir = ft.ElevatedButton(text='Inserir', style = x, on_click = self.inserir)
        btn_alterar = ft.ElevatedButton(text='Alterar',style = x, on_click = self.alterar)
        btn_eliminar = ft.ElevatedButton(text='Eliminar',style = x, on_click = self.eliminar)
        btn_listar = ft.ElevatedButton(text='Listar',style = x, on_click = self.listar)

        st = ft.Stack(
            controls = [
                ft.Container(
                    image_src = 'Imagens/Stars.png', 
                    image_fit = ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content = ft.Text(value = 'SpaceTicket', color = ft.colors.WHITE, size = 100),
                    top = 100,
                    left = 700,
                    alignment = ft.alignment.center,
                ),               
                ft.Container(
                    left = 0,
                    right = 570,
                    top = 525,

                    height = 180,
                    width = 1920,
                    image_src = 'Imagens/Inserir.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 0,
                    right = 180,
                    top = 515,

                    height = 200,
                    width = 1920,
                    image_src = 'Imagens/Alterar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ),
                ft.Container(
                    left = 200,
                    right = 0,
                    top = 480,

                    height = 270,
                    width = 1920,
                    image_src = 'Imagens/Deletar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    left = 575,
                    right = 0,
                    top = 530,

                    height = 170,
                    width = 1920,
                    image_src = 'Imagens/Consultar.png',  
                    opacity = 1,
                    padding=ft.padding.symmetric( horizontal=325),
                ), 
                ft.Container(
                    top = 500,
                    right = 500,
                    left = 500,
                    content = ft.Row(
                    controls = [
                         btn_isnerir,
                         btn_alterar,
                         btn_eliminar,
                         btn_listar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 100,
                        wrap = True,
                    ),
                ),
                ft.Container(
                    top = 900,
                    right = 300,
                    left = 300,
                    content = ft.Row(
                    controls = [
                        btn_voltar,
                        btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing = 800,
                        wrap = True,
                    ),
                ),
                
            ],
            expand = True,      
        )
        self.page.add(st)     
        self.main_page()
        
    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Menu 
    def voltar(self, e):
        self.page.clean()
        voltar = Principal(self.page)
        voltar.main_page()
    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Inserir dados na tabela Infracao
    def inserir(self, e):
        self.page.clean()
        inserir = InserirInfracao(self.page)
        inserir.main_page()
     # Ligação para Alterar dados na tabela Infracao
    def alterar(self, e):
        self.page.clean()
        alterar = AlterarInfracao(self.page)
        alterar.main_page()
    # Ligação para Eliminar dados na tabela Infracao   
    def eliminar(self, e):
        self.page.clean()
        eliminar = EliminarInfracao(self.page)
        eliminar.main_page()
    
    # Ligação para Listar dados da tabela Infracao
    def listar(self, e):
        self.page.clean()
        listar = ListarInfracao(self.page)
        listar.main_page()
    
    def main_page(self):
        pass
class Nave: #Funcional
    def __init__(self, page: ft.Page, return_to_menu=None):
        # Definição da classe Nave
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Estilo dos botões
        x = style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )
        # Botões
        btn_voltar = ft.ElevatedButton(text='Voltar', icon=ft.icons.ARROW_BACK_ROUNDED, style=x, on_click=self.voltar)
        btn_menu = ft.ElevatedButton(text='Menu', icon=ft.icons.MENU, style=x, on_click=self.abrir_menu)
        btn_documentacao = ft.ElevatedButton(text='Documentação', style=x, on_click=self.nave_documentacao_menu)
        btn_modelo = ft.ElevatedButton(text='Modelo', style=x, on_click=self.nave_modelo_menu)
        
        st = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png', 
                    image_fit=ft.ImageFit.FILL, 
                ), 
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),               
                ft.Container(
                    left=635,
                    right=0,
                    top=500,
                    height=450,
                    width=1920,
                    image_src='Imagens/NaveFinal.png',  
                    opacity=1,
                ),
                ft.Container(
                    left=0,
                    right=400,
                    top=535,
                    height=180,
                    width=1920,
                    image_src='Imagens/Historico.png',  
                    opacity=1,
                    padding=ft.padding.symmetric(horizontal=325),
                ), 
                ft.Container(
                    top=500,
                    right=500,
                    left=500,
                    content=ft.Row(
                        controls=[
                            btn_documentacao,
                            btn_modelo,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=300,
                        wrap=True,
                    ),
                ),
                ft.Container(
                    top=900,
                    right=300,
                    left=300,
                    content=ft.Row(
                        controls=[
                            btn_voltar,
                            btn_menu,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=800,
                        wrap=True,
                    ),
                ),
                
            ],
            expand=True,      
        )
        self.page.add(st)     
        self.main_page()

    # Ligação para Menu    
    def abrir_menu(self, e):
        self.page.clean()
        menu_principal = Principal(self.page)
        menu_principal.main_page()

    # Ligação para Menu 
    def voltar(self, e):
        self.page.clean()
        voltar = Principal(self.page)
        voltar.main_page()

    # Ligação para GuiaNaveDoc
    def nave_documentacao_menu(self, e):
        self.page.clean()
        nave_doc_menu = GuiaNaveDoc(self.page)
        nave_doc_menu.main_page()

    # Ligação para GuiaNaveMod 
    def nave_modelo_menu(self, e):
        self.page.clean()
        modelo_menu = GuiaNaveMod(self.page)
        modelo_menu.main_page()

    def main_page(self):
        pass

class Principal:#Funcional
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = 'SpaceTicket'
        self.page.window_maximized = True
        self.page.window_always_on_top = True
        self.page.padding = 0
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Habilitar chaves
        self.db_execute('PRAGMA foreign_keys = ON;')

        # Criar tabelas
        self.db_execute('CREATE TABLE IF NOT EXISTS Modelo(ID_Modelo INTEGER PRIMARY KEY AUTOINCREMENT, Cor TEXT, Formato TEXT, Motor TEXT);')
        self.db_execute('CREATE TABLE IF NOT EXISTS Nave(IDNave INTEGER PRIMARY KEY AUTOINCREMENT, QuantMaxPassageiros INTEGER, Deslocamento TEXT, NaveRoubada TEXT, ID_Modelo INTEGER, FOREIGN KEY (ID_Modelo) REFERENCES Modelo(ID_Modelo));')
        self.db_execute('CREATE TABLE IF NOT EXISTS Aparencia(Especie TEXT PRIMARY KEY, CorPele TEXT, QuantBracos INTEGER, QuantMaos INTEGER, QuantPernas INTEGER, QuantPes INTEGER, QuantCabecas INTEGER, QuantOlhos INTEGER, QuantChifres INTEGER, QuantCaudas INTEGER, QuantTentaculos INTEGER);')
        self.db_execute('CREATE TABLE IF NOT EXISTS Identificacao(IDSer INTEGER PRIMARY KEY AUTOINCREMENT, Nome TEXT, DataNascimento TIMESTAMP, Planeta TEXT, CartaDeConducao TEXT, ValidadeCarta TIMESTAMP, ConducaoPlanetaria TEXT, Especie TEXT, FOREIGN KEY (Especie) REFERENCES Aparencia(Especie));')
        self.db_execute('CREATE TABLE IF NOT EXISTS Infracao(IDInfracao INTEGER PRIMARY KEY AUTOINCREMENT, Valor INTEGER, Vencimento TIMESTAMP, Descricao TEXT, IDSer INTEGER, IDNave INTEGER, FOREIGN KEY (IDSer) REFERENCES Identificacao(IDSer), FOREIGN KEY (IDNave) REFERENCES Nave(IDNave));')

        # Elementos visuais da página
        self.create_ui_elements()

    def db_execute(self, query, params=[]):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall()

    def create_ui_elements(self):
        # Definindo o estilo dos botões
        button_style = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.BLACK,
            },
            bgcolor={
                ft.MaterialState.HOVERED: ft.colors.CYAN,
                ft.MaterialState.DEFAULT: ft.colors.AMBER,
            },
            padding={
                ft.MaterialState.HOVERED: 25,
                ft.MaterialState.DEFAULT: 25,
            },
        )

        # Criando os botões
        btn_nave = ft.ElevatedButton(text='Nave', style=button_style, on_click=self.nave_menu)
        btn_ident = ft.ElevatedButton(text='Identificação', style=button_style, on_click=self.identificacao_menu)
        btn_infra = ft.ElevatedButton(text='Infração', style=button_style, on_click=self.infracao_menu)

        # Criando a pilha de elementos
        stack = ft.Stack(
            controls=[
                ft.Container(
                    image_src='Imagens/Stars.png',
                    image_fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    content=ft.Text(value='SpaceTicket', color=ft.colors.WHITE, size=100),
                    top=100,
                    left=700,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    left=0,
                    right=635,
                    top=555,
                    height=450,
                    width=1920,
                    image_src='Imagens/NaveFinal.png',
                    opacity=1,
                ),
                ft.Container(
                    left=0,
                    right=50,
                    top=555,
                    height=250,
                    width=1920,
                    image_src='Imagens/Identificacao.png',
                    opacity=1,
                ),
                ft.Container(
                    left=820,
                    right=0,
                    top=595,
                    height=180,
                    width=1920,
                    image_src='Imagens/Historico.png',
                    opacity=1,
                    padding=ft.padding.symmetric(horizontal=325),
                ),
                ft.Container(
                    top=500,
                    right=500,
                    left=500,
                    content=ft.Row(
                        controls=[
                            btn_nave,
                            btn_ident,
                            btn_infra,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=300,
                        wrap=True,
                    ),
                ),
            ],
            expand=True,
        )

        # Adicionando a pilha de elementos à página
        self.page.add(stack)

    # Ligação para Nave
    def nave_menu(self, e):
        self.page.clean()
        nave = Nave(self.page)
        nave.main_page()

    # Ligação para Identificação
    def identificacao_menu(self, e):
        self.page.clean()
        identificacao = Identificacao(self.page)
        identificacao.main_page()

    # Ligação para Infração
    def infracao_menu(self, e):
        self.page.clean()
        infracao = GuiaInfra(self.page)
        infracao.main_page()

    def main_page(self):
        pass

if __name__ == '__main__':
    ft.app(target=Principal, assets_dir='Imagens')