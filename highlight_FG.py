import streamlit as st
from streamlit_ketcher import st_ketcher
from FGFinder import FindFG
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D


def moltosvg(smile,smart, molSize=(500,300),kekulize=True):
    _smile = Chem.MolFromSmiles(smile)
    matches = _smile.GetSubstructMatches(Chem.MolFromSmarts(smart))
    subs = []
    for i in matches:
        for j in i:
            subs.append(j)

    drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0],molSize[1])   
    drawer.DrawMolecule(_smile,highlightAtoms=subs)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText().replace('svg:','')
    return svg


st.write('UFG - LaCiQ - AZEVEDO, T. A. F.')
# Title.
st.title("What Chemical Functional Groups?")

# Imput the prompt to insert SMILES to work.
molecule = st.text_input('', 'CC(CCCO)O', placeholder='Paste the SMILES where')

# st_ketcher's Canvas, drawing the SMILE of prompt
smile_code = st_ketcher(molecule)

# Returns the SMILE of the drawing, in case of changes.
st.markdown('## SMILE: {}'.format(smile_code))

# Subtitle.
st.markdown('### Select functional groups for highlight ')

# DataFrame witch SMARTS in SMILE and frequency associate
fg = FindFG().findFunctionalGroups(smile_code)

# The checkbox corresponds to SMARTS and frequency
# when checking the checkbox, it shows a color choice box
for i in fg['Functional Groups']:
    column1, column2 = st.columns(2)
    freq = fg.at[fg[fg['Functional Groups'] == i].index[0], 'Frequency']
    smart = fg.at[fg[fg['Functional Groups'] == i].index[0], 'SMARTS']
    if column1.checkbox('{} {}'.format(freq, i), key='cb{}'.format(i)):
        mole = Chem.MolFromSmiles(smile_code)
        drawer = rdMolDraw2D.MolDraw2DSVG(400,200)
        drawer.DrawMolecule(mole,highlightAtoms=mole.GetSubstructMatch(Chem.MolFromSmarts(smart)))
        drawer.FinishDrawing()
        figure = moltosvg(smile_code, smart)
        st.image(figure)
