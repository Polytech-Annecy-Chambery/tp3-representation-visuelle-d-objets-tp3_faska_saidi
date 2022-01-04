# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""
import OpenGL.GL as gl

class Section:
    # Constructor
    def __init__(self, parameters = {}) :  
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        self.parameters = parameters
        
        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]        
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')   
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')   
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0              
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2 
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]       
        if 'edges' not in self.parameters:
            self.parameters['edges'] = False             
            
        # Objects list
        self.objects = []

        # Generates the wall from parameters
        self.generate()   
        
    # Getter
    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]
    
    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self     

    # Defines the vertices and faces 
    def generate(self):
        self.vertices = [ 
                [0, 0, 0 ], 
                [0, 0, self.parameters['height']], 
                [self.parameters['width'], 0, self.parameters['height']],
                [self.parameters['width'], 0, 0],
                [0,self.parameters['thickness'],0],
                [0,self.parameters['thickness'],self.parameters['height']],
                [self.parameters['width'],self.parameters['thickness'],self.parameters['height']],
                [self.parameters['width'],self.parameters['thickness'],0]
                ]
        self.faces = [
                [0, 3, 2, 1],
                [4,7,6,5],
                [0,3,7,4],
                [1,2,6,5],
                [3,7,6,2],
                [0,4,5,1]
                ]   

    # Checks if the opening can be created for the object x
    def canCreateOpening(self, x):
        L=x.parameters['width']+x.parameters['position'][0]
        H=x.parameters['height']+x.parameters['position'][2]
        return (L<=self.parameters['width']+self.parameters['position'][0] and H<=self.parameters['height']+self.parameters['position'][2])
        
    # Creates the new sections for the object x
    def createNewSections(self, x):
        #test si possibilité d'ouverture
        if self.canCreateOpening(x):
          #création liste de sortie
          new_section=[]
          #création des variables
          xS,yS,zS=self.parameters['position'][0],self.parameters['position'][1],self.parameters['position'][2]
          w=self.parameters['width']
          h=self.parameters['height']
          xO,zO=x.parameters['position'][0],x.parameters['position'][2]
          wO=x.parameters['width']
          hO=x.parameters['height']

          #test création de la section droite
          if xO-xS>0 :
            new_section.append(Section({'position':[xS,yS,zS], 'width': xO-xS, 'height': h}))

          #test création de la section gauche
          if (xS+w)-(xO+wO)>0:
            position=[(xO+wO),yS,0]
            new_section.append(Section({'position':position, 'width': (xS+w)-(xO+wO), 'height': h}))

          #test création de la section basse
          if (zO)-(zS)>0:
            position=[xO,yS,0]
            new_section.append(Section({'position':position, 'width': wO, 'height': (zO)-(zS)}))

          #test création de la section haute
          if (zS+h)-(zO+hO)>0:
            position=[xO,yS,(zO)-(zS)+hO]
            new_section.append(Section({'position':position, 'width': wO, 'height':  (zS+h)-(zO+hO)}))
        return new_section
            
        
    # Draws the edges
    def drawEdges(self):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)
        gl.glBegin(gl.GL_QUADS)
        gl.glColor3fv([0.25, 0.25, 0.25])
        gl.glVertex3fv([0, 0, 0])
        gl.glVertex3fv([self.parameters['width'], 0, 0])
        gl.glVertex3fv([self.parameters['width'], 0, self.parameters['height']])
        gl.glVertex3fv([0, 0, self.parameters['height']])
        gl.glEnd()  
    # Draws the faces
    def draw(self):
        if self.setParameter('edges', True):
          self.drawEdges()
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL) # on trace les faces : GL_FILL
        gl.glBegin(gl.GL_QUADS) # Tracé d’un quadrilatère
        gl.glColor3fv([0.5, 0.5, 0.5]) # Couleur gris moyen
        gl.glVertex3fv([0, 0, 0])
        gl.glVertex3fv([self.parameters['width'], 0, 0])
        gl.glVertex3fv([self.parameters['width'], 0, self.parameters['height']])
        gl.glVertex3fv([0, 0, self.parameters['height']])
        gl.glEnd()
  