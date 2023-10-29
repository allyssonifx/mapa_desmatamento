from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import random
import plotly.graph_objects as go

app = Flask(__name__)
# route -> hashtagtreinamentos.com/
# função -> o que você quer exibir naquela página
# template
def ler_tabela():
    df = pd.read_excel('dados_atualizacoes.xlsx')
    return df
def buscar_datas(df,nome):
    query = f'embargos =="{nome}"'
    infos  = df.query(query)
    return [infos['data_att'].iloc[0],infos['data_verif'].iloc[0],infos['data_prox'].iloc[0]]

def gerargrafico(df,dados):
    
    atts = ['AEG_DATA','AEI_DATA','DM_DATA','DA_DATA','DC_DATA','IA_DATA','IQ_DATA','LDIA_DATA','LDIM_DATA','LDIS_DATA','LESR_DATA','LSTB_DATA','MSP_DATA','PA_DATA','PC_DATA','PVG_DATA','SGPR_DATA','SGPU_DATA','SNPR_DATA','SNPU_DATA','TI_DATA','UC_DATA']
    emb = df['embargos']
    valores = df['tamanho']
    datas = ['05/01/2022','04/02/2022','01/03/2022','04/04/2022','01/05/2022','03/06/2022','03/07/2022','03/08/2022','03/09/2022','03/10/2022','03/11/2022','03/12/2022']

    dic = {}
    for c in range(0,len(emb)):
        val = float(valores[c])
        nums = []
        for _ in range(0,12):
            try:
                num = random.randint(-int(val*0.15), int(val*0.15))
            except:
                val = 10000
                num = random.randint(-int(val*0.001), int(val*0.15))
            val = val+num
            nums.append(val)
        dic[emb[c]] = nums
        dic[atts[c]] = datas
    df2 = pd.DataFrame(dic)
    
    fig = go.Figure(data=go.Scatter(x=df2[dados[0]], y=df2[dados[1]]))

    fig.update_layout(
        title='Quantidade de dados nos últimos 12 meses ' +dados[1],
        xaxis_title='DATAS',
        yaxis_title='Dados'
    )
    return fig


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/mapa")
def contatos():
    return render_template("mapa.html")

@app.route("/xx")
def conta():
    return render_template("pp.html")

@app.route('/grafico/<dado>')
def index(dado):
    dados = dado.split('-')
    df = ler_tabela()
    # Criando um gráfico de barras usando Plotly
    fig = gerargrafico(df,dados)

    datas = buscar_datas(df,dados[1])

    # Renderizando o gráfico no template HTML
    plot_div = fig.to_html(full_html=False)
    
    # Renderizando o template HTML com o gráfico
    return render_template('grafico.html', plot_div=plot_div,dado=dados[1],att=datas[0],ver=datas[1],pro=datas[2])

# colocar o site no ar
if __name__ == "__main__":
    app.run(debug=True)