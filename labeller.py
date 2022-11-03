from ast import While
from operator import index
from tkinter import Label
from tkinter.messagebox import NO
import pandas as pd
import inquirer
from tabulate import tabulate
import configparser
import os
import textwrap
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

def clear_screen():
    os.system('cls')

class Labeller:
 
    # init method or constructor
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.save = self.config['SAVES']

        self.currentIndex = int(self.save['lastIndex'])
        self.filename = self.save['filename']
        self.backup = self.save['backupfile']
        self.xlsx = pd.read_excel('juan.xlsx')
        self.savefile = pd.read_csv('juan.csv', index_col=0)

        self.currentRow = self.xlsx.iloc[self.currentIndex]
        self.currentLevel = self.currentRow['Level']
        self.currentObject = self.currentRow['Object']
        self.currentType = self.currentRow['Type']
        self.currentMeasurement = self.currentRow['Measurement']
        self.currentQuestion =  self.currentRow['Question']
        self.revisionRequired = "No"

        self.totalLen = self.xlsx.shape[0]
        self.unfinishedLen = str(int(self.totalLen) - int(self.currentIndex))

        self.updatedRow = pd.DataFrame()

    def _save(self):
        self.save['lastIndex'] = str(self.currentIndex)
        self.save['totalLen'] = str(self.xlsx.shape[0])

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        
        print('Exporting row ...')
        _exporting_csv = pd.concat([self.savefile, self.updatedRow], ignore_index=True)
        _exporting_csv.to_csv('juan.csv')
        
    def _get_last_index(self):
        return print(self.config['SAVES']['lastIndex'])

    def changeIndex(self, index):
        self.currentIndex = index

    def moveForward(self):
        self.currentIndex += 1
    
    def moveBackward(self):
        self.currentIndex -= 1

    def changeRow(self):
        self.currentRow = self.xlsx.iloc[self.currentIndex]
    
    def writeConfig(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def writeCSV(self):
        print('Writing CSV,',self.csv.shape, axis=0)
        self.csv.to_csv('juan.csv')
    
    def label(self):
        print(f'{"":=^40}\n\n')
        print('Editing Row No.: ', self.currentIndex)

        _rowdata = [[self.currentIndex, self.currentLevel, self.currentObject, self.currentType, self.currentMeasurement]]
        _rowhead = ['index','Level','Object','Type','Measurement']
        _question = [[self.currentQuestion]]

        question_data = (tabulate(_rowdata, headers=_rowhead, tablefmt="grid"))
        
        print(question_data)
        print(f'\n{" Question ":=^40}')
        # print('\n', _question[0][0], '\n')

        wrapper = textwrap.TextWrapper(width=80)
        word_list = wrapper.wrap(text=_question[0][0])
        print()
        for element in word_list:
            print(element)
        print(f'\n{"":=^40}\n\n')

        main_menu = [inquirer.List("menu", message="What to do with this datum?", choices=["Edit", "Skip", "Choose Index"]),]
        menu = inquirer.prompt(main_menu)

        if menu['menu'] == 'Choose Index':
            print('Feature not implemented.')
            clear_screen()
            self.__init__()
            
            # index_change = [inquirer.Text("index_change", message="Which index? (0-799)")]
            # index_answer = inquirer.prompt(index_change)
            # edit_df = pd.read_csv('juan.csv')
            # edit_row = edit_df.iloc[int(index_answer['index_change'])]
            # # edit_row = pd.DataFrame([[edit_row['Level'], edit_row['Object'], edit_row['Type'], edit_row['Measurement'], edit_row['Question'], 'Yes', 'No']], columns=['Level','Object','Type','Measurement','Question','Answerable', 'Revision'])
            # print(edit_row)

            # print('Editing :', index_answer['index_change'],'\n')

            # editor_level_answer = [inquirer.List("Level", message="Which is the appropriate level?", choices=["Easy", "Medium", "Difficult"],),]
            # editor_currentLevel = inquirer.prompt(editor_level_answer)
            # print('Level set to:', editor_currentLevel['Level'],'\n')

            # editor_object = [inquirer.Text("Object", message="What is the object?")]
            # editor_currentObject = inquirer.prompt(editor_object)
            # print('Object set to:', editor_currentObject['Object'],'\n')

            # editor_type_answer = [inquirer.List("Type", message="What is the dimension?", choices=["2D", "3D"],),]
            # editor_currentType = inquirer.prompt(editor_type_answer)
            # print('Type set to:', editor_currentType['Type'],'\n')

            # editor_measurement_answer = [inquirer.List("Measurement", message="What is being measured?", choices=["Area", "Surface area", "Perimeter", "Angle", "Dimension", "Volume"],),]
            # editor_currentMeasurement = inquirer.prompt(editor_measurement_answer)
            # print('Measurement set to:', editor_currentMeasurement['Measurement'],'\n')

            # editor_mark_revision = [inquirer.List("Revision", message="Want to change the question later?", choices=["No", "Yes"],),]
            # editor_revisionRequired = inquirer.prompt(editor_mark_revision)
            # print('Given revision marker:', editor_revisionRequired['Revision'],'\n')

            # edited_row = [editor_currentLevel['Level'], editor_currentObject['Object'], editor_currentType['Type'], editor_currentMeasurement['Measurement'], edit_row['Question'], 'Yes', editor_revisionRequired['Revision']]
            # edit_df.iloc[int(index_answer['index_change'])] = edited_row
            # edit_df.to_csv('juan.csv', index=False)
            # print('Done!')
            # self.label()

        elif menu['menu'] == 'Skip':
            print("Skipping ... ")
            self.updatedRow = pd.DataFrame([[self.currentLevel, self.currentObject, self.currentType, self.currentMeasurement, self.currentQuestion, 'Yes', 'No']], columns=['Level','Object','Type','Measurement','Question','Answerable', 'Revision'])
            print(self.updatedRow)
            self.moveForward()
            self._save()
            self.changeRow()
            self.__init__()
            
        elif menu['menu'] == 'Edit':
            
            level_answer = [inquirer.List("Level", message="Which is the appropriate level?", choices=["Easy", "Medium", "Difficult"],),]
            self.currentLevel = inquirer.prompt(level_answer)
            print('Level set to:', self.currentLevel['Level'],'\n')

            object = [inquirer.Text("Object", message="What is the object?")]
            self.currentObject = inquirer.prompt(object)
            print('Object set to:', self.currentObject['Object'],'\n')

            type_answer = [inquirer.List("Type", message="What is the dimension?", choices=["2D", "3D"],),]
            self.currentType = inquirer.prompt(type_answer)
            print('Type set to:', self.currentType['Type'],'\n')

            measurement_answer = [inquirer.List("Measurement", message="What is being measured?", choices=["Surface area", "Perimeter", "Angle", "Dimension", "Volume"],),]
            self.currentMeasurement = inquirer.prompt(measurement_answer)
            print('Measurement set to:', self.currentMeasurement['Measurement'],'\n')

            mark_revision = [inquirer.List("Revision", message="Want to change the question later?", choices=["No", "Yes"],),]
            self.revisionRequired = inquirer.prompt(mark_revision)
            print('Given revision marker:', self.revisionRequired['Revision'],'\n')

            self.updatedRow = pd.DataFrame([[self.currentLevel['Level'], (str(self.currentObject['Object']).casefold().title()), self.currentType['Type'], self.currentMeasurement['Measurement'], self.currentQuestion, 'Yes', self.revisionRequired['Revision']]], columns=['Level','Object','Type','Measurement','Question','Answerable', 'Revision'])
            print(self.updatedRow)
            self.moveForward()
            self._save()
            self.changeRow()
            self.__init__()

        
    
 
if __name__ == '__main__':

    l = Labeller()
    while True:
        l.label()
        clear_screen()