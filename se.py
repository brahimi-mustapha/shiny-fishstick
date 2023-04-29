import copy

import wx
class Regle:
    def __init__(self, premises, conclusion):
        self.premises = premises
        self.conclusion = conclusion
        self.used = False


regles = [
    
    Regle(['A', 'B'], 'F'),
    Regle(['F', 'H'], 'I'),
    Regle(['D', 'H', 'G'], 'A'),
    Regle(['O', 'G'], 'U'),
    Regle(['E', 'H'], 'B'),
    Regle(['G', 'A'], 'B'),
    Regle(['G', 'H'], 'P'),
    Regle(['G', 'H'], 'Q'),
    Regle(['D', 'G', 'G'], 'J'),
    Regle(['D', 'G', 'U'], 'W')
]


class MoteurInference:

    def __init__(self, baseFait ):
        self.baseFait = baseFait
        self.regles = copy.deepcopy(regles)

    def chainageAvant(self):
        nouveauxFaits = True
        gestionDeConflicts = []
        while nouveauxFaits:
            nouveauxFaits = False
            for regle in self.regles:
                if( regle.used ):
                    continue
                if self.toutesLesPremissesSontVraies( regle ):
                    gestionDeConflicts.append(regle)

            if( len( gestionDeConflicts ) > 0 ):

                gestionDeConflicts.sort(key=lambda x: len( x.premises ), reverse=False)

                regle = gestionDeConflicts.pop()
                regle.used = True
                if regle.conclusion not in self.baseFait:
                    self.baseFait[regle.conclusion] = True
                    nouveauxFaits = True



    def toutesLesPremissesSontVraies(self, regle):
        for premisses in regle.premises:
            if premisses not in self.baseFait or not self.baseFait[premisses]:
                return False
        return True

########################################################################
class MyPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent)
    
########################################################################
class MyFrame(wx.Frame):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):


        wx.Frame.__init__(self, None, title="Project Tech Agent")
        panel = MyPanel(self)
        self.panel = panel

        self.Show()
        self.Maximize(True)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("app.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        "checkboxes"

        self.premises = set()

        for regle in regles:
            for premise in regle.premises:
                self.premises.add( premise )



        st = wx.StaticText(panel, label ="Construire la base de faits", pos = (38, 38))

        self.checkboxes = [0] * len( self.premises )

        for i, premise in enumerate(self.premises):
            self.checkboxes[i] = wx.CheckBox(panel, label = f'  {premise}', pos = (38, (i + 2)* 38)) 


        self.resolveButton = wx.Button(panel, label='Solve', pos=(38, (len(self.premises) + 2)* 38))


        "Choisir votre but"

        terms = self.premises.copy()

        for regle in regles:
            terms.add( regle.conclusion )


        self.butTitle = wx.StaticText(panel, label="Choisir votre but", pos = (250, 38))
        self.but = wx.ComboBox(panel, pos = (250, 38 * 2), choices=list(terms)); 
        self.resultTitle = wx.StaticText(self.panel, pos = (250, 38 * 3))

        "Solve the problem"

        self.resolveButton.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, e): 

        baseFait = {}
        
        for i, premise in enumerate( self.premises ):
            if( self.checkboxes[i].IsChecked() ):
                baseFait[premise] = True

        moteur = MoteurInference(baseFait)
        moteur.chainageAvant()
        but = self.but.GetValue()
        estVrai = moteur.baseFait[but] if but in moteur.baseFait else False

        if( len(but) > 0 ):
            self.resultTitle.SetLabel( but + ' est ' + str(estVrai) )
        else:
            self.resultTitle.SetLabel( "s'il vous plais choisir un but" )



if __name__ == '__main__':
    baseFait = {'D': True, 'G': True, 'U': True}
    moteur = MoteurInference(baseFait)
    moteur.chainageAvant()
    fait = 'W'
    estVrai = moteur.baseFait[fait] if fait in moteur.baseFait else False
    print(fait + ' est ' + str(estVrai))
    print( moteur.baseFait )


    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()