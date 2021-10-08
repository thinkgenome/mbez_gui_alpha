import os
import sys
import subprocess


if sys.platform == 'darwin': # for MacOs
    cmd = 'chmod 755'
    cmd1 = 'chmod 755 installer.sh'
    cmd2 = 'chmod 755 16Spipeline_qiime2v2019v4docker_gui_v1.sh'
    cmd3 = 'chmod 755 mebigeasy-bigmex.sh'
    cmd4 = 'chmod 755 taxfunc.sh'
    cmd5 = 'chmod 755 mebigeasy-shotgundomain.sh'
    os.system(cmd)
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    installer = os.path.abspath('installer.sh')
    print(installer)
    subprocess.call(installer, shell=True)
elif sys.platform in ["linux", "linux2"]: # for Linux
    cmd = 'chmod 755'
    cmd1 = 'chmod 755 installer.sh'
    cmd2 = 'chmod 755 16Spipeline_qiime2v2019v4docker_gui_v1.sh'
    cmd3 = 'chmod 755 mebigeasy-bigmex.sh'
    cmd4 = 'chmod 755 taxfunc.sh'
    cmd5 = 'chmod 755 mebigeasy-shotgundomain.sh'
    os.system(cmd)
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    installer = os.path.abspath('installer.sh')
    print(installer)
    subprocess.call(installer, shell=True)
#elif sys.platform in ["win32", "cygwin"]: # for Windows
 #   pass
else: # for windows
    cmd1 = 'icacls "installer.sh" /grant %username%:(OI)(CI)F /T'
    cmd2 = 'icacls "16Spipeline_qiime2v2019v4docker_gui_v1.sh" /grant %username%:(OI)(CI)F /T'
    cmd3 = 'icacls "mebigeasy-bigmex.sh" /grant %username%:(OI)(CI)F /T'
    cmd4 = 'icacls "taxfunc.sh" /grant %username%:(OI)(CI)F /T'
    cmd5 = 'icacls "mebigeasy-shotgundomain.sh" /grant %username%:(OI)(CI)F /T'
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    installer = os.path.abspath('installer.sh')
    print(installer)
    subprocess.call(installer, shell=True)


# standard library imports
import getpass
import time
import shutil
import uuid
import fnmatch
import zipfile
import glob
import webview
from concurrent import futures
import pandas as pd
import linecache
import webbrowser




# import of kivy configurations
from kivy.config import Config

# set of kivy configurations
from kivy.uix import filechooser, screenmanager

Config.set('kivy', 'desktop', 1)
Config.set('kivy', 'exit_on_escape', 0)
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'height', 700)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'minimum_height', 700)
Config.set('graphics', 'minimum_width', 1000)
Config.set('graphics', 'resizable', True)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1) # used to run analyses in the background, max_workers decides how many analyses can run at the same time


class ScreenManagement(ScreenManager):
    screenmanager = ScreenManager()
    pass


class ProbarPopup(Popup):
    pop_up_text = ObjectProperty()

    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message


class NewPipelinenamePopup(Popup):
    newpipe_text = ObjectProperty()

    def update_newpipe_text(self, p_message):
        self.newpipe_text.text = p_message



class ProjectnamePopup(Popup): # takes text input from user and saves it in a varialble
    project_name_text_input = ObjectProperty()
    projectname = StringProperty('')
    projectdisplay = StringProperty()

    def get_projectname(self):
        self.projectname = self.project_name_text_input.text  # set projectname to text put in in TextInput
        print('{}'.format(self.projectname))
        self.save()
        global getter
        getter = self.projectname
        return self.projectname

    def get_projectdisplay(self):
        self.projectdisplay = getter


    def save(self): # saves string from textinput in a text file
        with open('projectname.txt', 'w') as saver:
            saver.write(str(self.projectname))

    def load(self): # opens textfile created in self and returns copy of containing string (rstring)
        with open('projectname.txt') as fobj:
            for projectname in fobj:
                self.projectname = projectname.rstrip()



class PipelinenamePopup(Popup): # takes text input from user and saves it in a varialble
    pipeline_name_text_input = ObjectProperty()
    pipelinename = StringProperty('')
    pipelinedisplay = StringProperty()



    def get_pipelinename(self):
        self.pipelinename = self.pipeline_name_text_input.text  # set projectname to text put in in TextInput
        print('{}'.format(self.pipelinename))
        self.save()
        global getter
        getter = self.pipelinename
        if self.check_pipelinename() is True:
            return self.pipelinename

    def get_pipelinedisplay(self):
        self.pipelinedisplay = getter



    def save(self): # saves string from textinput in a text file
        with open('pipelinename.txt', 'w') as saver:
            saver.write(str(self.pipelinename))

    def load(self): # opens textfile created in self and returns copy of containing string (rstring)
        with open('pipelinename.txt') as fobj:
            for projectname in fobj:
                self.pipelinename = projectname.rstrip()

    def check_pipelinename(self):
        projectfolder = os.path.abspath('Projects')
        projects = glob.glob('%s/*_mebigeasy' % projectfolder)
        pipename = self.pipelinename + '_mebigeasy'
        pipepath = os.path.abspath('Projects/%s' % pipename)
        for root, dirs, files in os.walk(projectfolder):
            projects
        if os.path.getsize(os.path.abspath('pipelinename.txt')) > 0:
            if pipepath not in projects:
                return True
            else:
                self.newpipe_pop = Factory.NewPipelinenamePopup()
                self.newpipe_pop.update_newpipe_text('Projectname already taken, choose new one')
                self.newpipe_pop.open()

        else:
            self.newpipe_pop = Factory.NewPipelinenamePopup()
            self.newpipe_pop.update_newpipe_text('Must insert Projectname')
            self.newpipe_pop.open()



class ProjectnamePopupShotgun(Popup): # takes text input from user and saves it in a varialble
    project_name_text_input = ObjectProperty()
    projectname = StringProperty('')

    def get_projectname(self):
        self.projectname = self.project_name_text_input.text  # set projectname to text put in in TextInput
        print('{}'.format(self.projectname))
        self.save()
        return self.projectname

    def save(self): # saves string from textinput in a text file
        with open('projectname.txt', 'w') as saver:
            saver.write(str(self.projectname))

    def load(self): # opens textfile created in self and returns copy of containing string (rstring)
        with open('projectname.txt') as fobj:
            for projectname in fobj:
                self.projectname = projectname.rstrip()


class ProjectnamePopupResult(Popup): # takes text input from user and saves it in a varialble
    project_name_text_input = ObjectProperty()
    projectname = StringProperty('')

    def get_projectname(self):
        self.projectname = self.project_name_text_input.text  # set projectname to text put in in TextInput
        print('{}'.format(self.projectname))
        self.save()
        return self.projectname

    def save(self): # saves string from textinput in a text file
        with open('projectname.txt', 'w') as saver:
            saver.write(str(self.projectname))

    def load(self): # opens textfile created in self and returns copy of containing string (rstring)
        with open('projectname.txt') as fobj:
            for projectname in fobj:
                self.projectname = projectname.rstrip()


class SixteenslogPopup(Popup):
    data = StringProperty()
    bgcdata = StringProperty()

    def __init__(self, **kwargs):
        super(SixteenslogPopup, self).__init__(**kwargs)
        self.data = ''
        #self.get_log()
        Clock.schedule_interval(self.get_last_n_loglines, 1)

    '''def get_log(self, dt):
        if os.path.exists(os.path.abspath('log.txt')):
            with open('log.txt', 'r') as log:  # gets the string from .txt file and makes it useable
                self.data = log.read()
                self.data = self.data.replace('b', '')
                #print(self.data)
        #threading.Timer(1, self.get_log).start()'''

    def get_last_n_loglines(self, dt):
        with open('log.txt', 'r') as file:
            for line in (file.readlines()[-10:]):
                self.data = line
                self.data = self.data.replace("b'", "")
                self.data = self.data.replace("'", "")

           # self.data = self.data.replace("b'", "")




class MeBigEasy(App):

    #stop = threading.Event()

    # ++++++++++++++++++++++++++++++++++++++++++
    # GUI RELATED VARIABLES
    # +++++++++++++++++++++++++++++++++++++++++++
    csv_view = ListProperty()
    importchooser = StringProperty()
    exportchooser = ObjectProperty(None)
    screenmanager = ScreenManager()
    namer1 = StringProperty()

    # variables for other classes (used to call functions from these classes in .kv)
    pipelinename_popup = PipelinenamePopup()
    projectname_popup = ProjectnamePopup()


    # used to display sixteens analysis status
    sixteenschecker = NumericProperty(0) # is zero when no Analysis is running
    sixteensstatus = StringProperty()

    # used to display bgc analysis status
    bgcchecker = NumericProperty(0) # is zero when no Analysis is running
    bgcstatus = StringProperty()

    # used to display shotgun metagenome analysis status
    shotgunchecker = NumericProperty(0) # is zero when no Analysis is running
    shotgunstatus = StringProperty()

    # used to display previews of png files embedded in the gui
    previewsource = ObjectProperty(None)

    # used to display the shell file used in the custom pipeline
    customshell = StringProperty()

    # used to display selected pipelinename/manifest etc
    sixteensmanifestdisplay = StringProperty()
    sixteensfastqdisplay = StringProperty()
    sixteensmetadatadisplay = StringProperty()

    bgcmanifestdisplay = StringProperty()
    bgcfastqdisplay = StringProperty()

    shotguntaxmanifestdisplay = StringProperty()
    shotguntaxfastqdisplay = StringProperty()

    shotgundommanifestdisplay = StringProperty()
    shotgundomfastqdisplay = StringProperty()


    # used to display selected files in filechooser
    sixteensmanifestchooser = StringProperty()
    metadatachooser = StringProperty()


    # +++++++++++++++++++++++++++++++++++++++++++
    # GUI RELATED FUNCTIONS
    # +++++++++++++++++++++++++++++++++++++++++++

    def __init__(self, **kwargs):
        super(MeBigEasy, self).__init__(**kwargs)
        self.sixteenschecker = 0
        self.bgcchecker = 0
        Clock.schedule_interval(self.check_sixteens_analysis, 1)
        Clock.schedule_interval(self.check_bgc_analysis, 1)
        Clock.schedule_interval(self.check_shotgun_analysis, 1)


    def build(self):
        presentation = Builder.load_file("mebigez.kv")
        #Window.bind(on_request_close = self.on_request_close) # calls closepopup when hitting the close button
        return presentation



    def on_request_close(self, *args):
        self.closepopup(title='Exit', text='Are you sure you want to quit? \n All result files will be deleted')
        return True
        
    def closepopup(self, title='', text=''):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))
        releasebutton = Button(text='Yes')
        staybutton = Button(text='Back')
        box2 = BoxLayout(orientation='horizontal', spacing=5)
        box2.add_widget(releasebutton)
        box2.add_widget(staybutton)
        box.add_widget(box2)
        popup = Popup(title=title, content=box, size_hint=(None, None), size=(500, 300), pos_hint={'center_x':.5, 'center_y': .5})
        releasebutton.bind(on_release=self.stop) # Button to close the window 
        staybutton.bind(on_release=popup.dismiss) # Button to stay in window
        popup.open()

    def show_probar_popup(self):  # progressbar popup
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('Loading...')
        self.pop_up.open()

    '''def show_newline_popup(self):
        self.newpipe_pop = Factory.NewPipelinenamePopup()
        self.newpipe_pop.update_newpipe_text('Projectname already taken, choose new one')
        self.newpipe_pop.open()'''



    '''def whichrun(self, filename):  # checks wether a new analysis or results are supposed to be run
        if self.forbid_sixteens() is False:
            print('16srun')
            global chosenfile
            chosenfile = '%s' % filename[0]
            if chosenfile.endswith('.qzv'):
                Factory.ImportFiles().dismiss()
                self.run_results(filename)
            elif chosenfile.endswith('data'):
                #self.sixteens_progress_bar(filename)
                self.run_sixteens(filename)
            elif self.check_shell() is True:
                self.run_custom(filename)
            else:
                #self.sixteens_progress_bar(filename)
                self.run_sixteens(filename)
                #self.pop_up = Factory.ProbarPopup()
                # self.pop_up.update_pop_up_text('File is neither .qzv, nor .sh or manifest-data')
        else:
            print('bgcrun')
            global bgcfile
            bgcfile = '%s' % filename[0]
            global bgcbase
            bgcbase = os.path.basename(bgcfile)
            self.run_bgc(filename)
        Factory.AnalysisPopup().open()'''

    '''def whichrun_sixteens(self):
        global chosenfile
        if self.check_manifest_sixteens() is True:
            print('16s run')
            chosenfile = sixteensmanifest
            print(chosenfile)
            self.run_sixteens()

    def whichrun_bgc(self):
        global bgcfile
        if self.check_manifest_bgc() is True:
            bgcfile = bgcmanifest
            global bgcbase
            bgcbase = os.path.basename(bgcfile)
            self.run_bgc()'''






    def try_filename(self, filename):
        try:
            filename[0]
        except IndexError:
            return False
        else:
            return True


    '''def whichrun_shotgun(self, filename):
        if self.forbid_shotguntaxprofiling() is False:
            print('shotguntax run')
            global shotguntaxfile
            shotguntaxfile = '%s' % filename[0]
            self.run_shotgun_taxonomy(filename)
        else:
            print('shotgundomain run')
            global shotgundomainfile
            shotgundomainfile = '%s' % filename[0]
            self.run_shotgun_domain(filename)
        Factory.AnalysisPopup().open()'''


    # +++++++++++++++++++++++++++++++++++++++++++
    # 16s RUN FUNCTIONS
    # +++++++++++++++++++++++++++++++++++++++++++

    def run_sixteens(self):  # runs the 16s analysis and updates the sixteens progressbar when finished
        global chosenfile
        chosenfile = sixteensmanifest
        self.delete_preview_png() # empties preview dir to make room for new files
        self.set_sixteenschecker_zero()
        self.sixteenschecker = self.sixteenschecker + 1
        self.change_shell_manifest()  # changes the manifest data name in the shell file
        self.change_shell_metadata() # changes the sample-metadata name in the shell file
        self.place_manifest()
        self.place_metadata()
        self.place_fastq()
        thread_pool_executor.submit(self.sixteens_analysis)

    def sixteens_analysis(self): # runs the sixteeens analysis, has to be an isolated method because it has to be run in background (no filename variable attached)
        print('sixteens_analysis')
        self.sixteenschecker = self.sixteenschecker + 1
        self.create_pipelinefolder()
        self.create_projectfolder()
        self.get_pipelinename()
        self.get_jobname()
        self.configurate_sixteens_shell()
        #self.set_sixteenschecker_zero()
        global sixteensuserpath
        sixteensuserpath = pipestring + '_mebigeasy'
        global sixteensresultpath  # gives path to view result files even when multiple jobs were executed
        sixteensresultpath = os.path.abspath(sixteensuserpath)
        print(sixteensresultpath)
        start_time = time.time()
        print(start_time)
        a = os.path.abspath('16Spipeline_qiime2v2019v4docker_gui_v1.sh')
        proc = subprocess.Popen([a], shell=True, stdout=subprocess.PIPE)
        if os.path.exists(os.path.abspath('log.txt')):
            startstring = open('log.txt', 'wt')
            startstring.write('16s Analysis started \n')
            startstring.close()
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line.rstrip(), file = open('log.txt', 'a'))
            print(line.rstrip())
        print('Analysis completed succesfully', file=open('log.txt', 'a'))

        self.unzip_sixteens()
        self.rename_logfile()
        for _ in range(14):
            self.rename_resultfolder()
            self.move_result_files()
            self.move_sixteens_folders()
            self.move_projectfolder()  # moves sixteens_folder in project folder
            self.move_logfile()
            self.rename_index()
            self.rename_permanovapairwise()
            self.rename_kruskallayer()
            self.rename_kruskalsite()
            self.rename_metadata()
        self.move_jobfolder()
        self.setback_configfile() # sets config-file.txt back to default
        #self.undo_change_shell()  # after Analysisis complete, renames the manifest-data file, so new Analysis can be started
        self.delete_sixteensshell()
        self.replace_sixteensshell()
        #self.move_preview_files_sixteens()
        self.get_htmlhyperlinks_sixteens()
        self.get_csv_sixteenspreview()
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('16s-Analysis completed succesfully')
        self.pop_up.open()
        print('16s Analysis finished in ', (time.time() - start_time)/3600, 'h')
        print('16s Analysis finished in ', (time.time() - start_time)/60, 'm')
        self.sixteenschecker = self.sixteenschecker + 1


    def run_results(self, filename):  # shows results of a chosen .qzv file without running the whole process
        print('Result Run')
        global chosenresult
        chosenresult = '%s' % filename[0]
        self.create_pipelinefolder()
        self.create_projectfolder()
        self.get_pipelinename()
        self.get_jobname()
        global sixteensuserpath
        sixteensuserpath = pipestring + '_' + 'mebigeasy'
        global sixteensresultpath  # gives path to view result files even when multiple jobs were executed
        sixteensresultpath = os.path.abspath(sixteensuserpath)
        self.place_result(filename)
        self.unzip_sixteens()
        for _ in range(14):
            self.rename_resultfolder()
            self.move_result_files()
            self.move_sixteens_folders()
            self.move_projectfolder()  # moves sixteens_folder in projectfolder
            self.rename_index()  # if created renames index.html file to unique index file
            self.rename_permanovapairwise()
            self.rename_kruskallayer()
            self.rename_kruskalsite()
            self.rename_metadata()
        self.move_jobfolder()
        #self.move_preview_files_sixteens()
        #self.get_csv_sixteenspreview()
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('Results loaded succesfully')
        self.pop_up.open()


    def reset_sixteens(self): # resets the manifestdisplay, sixteensmanifestchooser etc., also deletes the imported files to make new analysis possible
        if self.sixteenschecker == 0 or self.sixteenschecker == 3:
            self.set_sixteenschecker_zero()
            self.sixteensmanifestchooser = ''
            self.sixteensmanifestdisplay = ''
            self.metadatachooser = ''
            self.sixteensmetadatadisplay = ''
            self.sixteensfastqdisplay = ''
            self.empty_jobname() # empties the jobname file the file
            self.projectname_popup.projectdisplay = ''
            self.delete_files_reset_sixteens()
            self.delete_fastq_sixteens()
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text("Can't reset during Analysis")
            self.pop_up.open()



    # +++++++++++++++++++++++++++++++++++++++++++
    # BGC Taxonomy Run Functions
    # +++++++++++++++++++++++++++++++++++++++++++

    def run_bgc(self):
        global bgcfile
        bgcfile = bgcmanifest
        global bgcbase
        bgcbase = os.path.basename(bgcfile)
        self.set_bgcchecker_zero()
        self.bgcchecker = self.bgcchecker + 1
        self.place_manifest()
        self.place_fastq()
        self.get_namers()
        thread_pool_executor.submit(self.bgc_analysis)

    def bgc_analysis(self):
        print('bgc_analysis')
        self.bgcchecker = self.bgcchecker + 1
        self.create_projectfolder()
        self.create_pipelinefolder()
        self.get_jobname()
        self.get_pipelinename()
        global bgcuserpath
        bgcuserpath = pipestring + '_' + 'mebigeasy'
        global bgcresultpath  # gives path to view result files even with multiple jobs run
        bgcresultpath = os.path.abspath(bgcuserpath)
        starttime = time.time()
        shellfile = os.path.basename(os.path.abspath('mebigeasy-bigmex.sh'))
        runfile = os.path.basename(bgcfile)
        bgcanalysis = './' + shellfile + ' ' + runfile + ' ' + domainname  # gives the command the shell file needs to run
        proc = subprocess.Popen([bgcanalysis], shell=True, stdout=subprocess.PIPE)
        if os.path.exists(os.path.abspath('log.txt')):
            startstring = open('log.txt', 'wt')
            startstring.write('BGC Analysis started \n Command: %s \n' % bgcanalysis)
            startstring.close()
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line.rstrip(), file=open('log.txt', 'a'))
            print(line.rstrip())
        print('Analysis completed succesfully', file=open('log.txt', 'a'))

        self.rename_logfile
        #subprocess.call([bgcanalysis], shell=True)
        for _ in range(3):
            self.rename_resultfolder()
            self.move_result_files()
            self.move_projectfolder()
            self.move_logfile()
            self.rename_placementstree()
            self.rename_violin()
            self.rename_bindigsummary()
            self.rename_bindigmodel()
            self.rename_bindigcluster()
            self.rename_bindingquery()
        print('BGC-Analysis finished in ', (time.time() - starttime) / 3600, 'h')
        self.move_jobfolder()
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('BGC-Analysis completed succesfully')
        self.pop_up.open()
        self.bgcchecker = self.bgcchecker + 1


    def reset_bgc(self): # resets the bgcmanifestdisplay,bgcmanifestchooser etc., also deletes the imported files to make new analysis possible
        if self.bgcchecker == 0 or self.bgcchecker == 3:
            self.set_bgcchecker_zero()
            self.bgcmanifestchooser = ''
            self.bgcmanifestdisplay = ''
            self.bgcfastqdisplay = ''
            self.empty_jobname() # empties the jobname file the file
            self.projectname_popup.projectdisplay = ''
            self.delete_files_reset_bgc()
            self.delete_fastq_bgc()
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text("Can't reset during Analysis")
            self.pop_up.open()


    # +++++++++++++++++++++++++++++++++++++++++++
    # Shotgun Taxonomy Run Functions
    # +++++++++++++++++++++++++++++++++++++++++++

    def run_shotgun_taxonomy(self):
        global shotguntaxfile
        shotguntaxfile = shotguntaxmanifest
        self.set_shotgunchecker_zero()
        self.shotgunchecker = self.shotgunchecker + 1
        self.place_manifest()
        self.place_fastq()
        self.get_namers()
        thread_pool_executor.submit(self.shotgun_taxonomy_analysis)

    def shotgun_taxonomy_analysis(self):
        print('shotgun_taxonomy_analysis')
        self.shotgunchecker = self.shotgunchecker + 1
        self.create_projectfolder()
        self.create_pipelinefolder()
        self.get_jobname()
        self.get_pipelinename()
        global shotgunuserpath
        shotgunuserpath = pipestring + '_' + 'mebigeasy'
        global shotgunresultpath  # gives path to view result files even with multiple jobs run
        shotgunresultpath = os.path.abspath(shotgunuserpath)
        start_time = time.time()
        print(start_time)
        shellfile = os.path.basename(os.path.abspath('taxfunc.sh'))
        runfile = os.path.basename(shotguntaxfile)
        shotgunanalysis = './' + shellfile + ' ' + runfile   # gives the command the shell file needs to run
        print(shotgunanalysis)
        #subprocess.call([shotgunanalysis], shell=True)
        proc = subprocess.Popen([shotgunanalysis], shell=True, stdout=subprocess.PIPE)
        if os.path.exists(os.path.abspath('log.txt')):
            startstring = open('log.txt', 'wt')
            startstring.write('Shotgun Taxonomy Analysis started \n Command: %s \n' % shotgunanalysis)
            startstring.close()
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line.rstrip(), file=open('log.txt', 'a'))
            print(line.rstrip())
        print('Analysis completed succesfully', file=open('log.txt', 'a'))

        self.move_shotgun_results()  # moves the results fastq files created in shotgun taxonomy analysis to the Projectfolder
        self.move_jobfolder()
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('Shotgun Metagenome-Analysis completed succesfully')
        self.pop_up.open()
        print('Shotgun Taxonomy Analysis finished in ', (time.time() - start_time) / 3600, 'h')
        self.shotgunchecker = self.shotgunchecker + 1

    def reset_shotguntax(self): # resets the bgcmanifestdisplay,bgcmanifestchooser etc., also deletes the imported files to make new analysis possible
        if self.shotgunchecker == 0 or self.shotgunchecker == 3:
            self.set_shotgunchecker_zero()
            self.shotguntaxmanifestdisplay = ''
            self.shotguntaxfastqdisplay = ''
            self.empty_jobname() # empties the jobname file the file
            self.projectname_popup.projectdisplay = ''
            self.delete_files_reset_shotguntax()
            self.delete_fastq_shotguntax()
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text("Can't reset during Analysis")
            self.pop_up.open()


    # +++++++++++++++++++++++++++++++++++++++++++
    # Shotgun Domain Run Functions
    # +++++++++++++++++++++++++++++++++++++++++++
    def run_shotgun_domain(self, ):
        global shotgundomainfile
        shotgundomainfile = shotgundommanifest
        self.set_shotgunchecker_zero()
        self.shotgunchecker = self.shotgunchecker + 1
        self.place_manifest()
        self.place_fastq()
        self.get_namers()
        thread_pool_executor.submit(self.shotgun_domain_analysis)

    def shotgun_domain_analysis(self):
        print('shotgun_domain_analysis')
        self.shotgunchecker = self.shotgunchecker + 1
        self.create_projectfolder()
        self.create_pipelinefolder()
        self.get_jobname()
        self.get_pipelinename()
        global shotgunuserpath
        shotgunuserpath = pipestring + '_' + 'mebigeasy'
        global shotgunresultpath  # gives path to view result files even with multiple jobs run
        shotgunresultpath = os.path.abspath(shotgunuserpath)
        start_time = time.time()
        print(start_time)
        shellfile = os.path.basename(os.path.abspath('mebigeasy-shotgundomain.sh')) # same as bgc
        runfile = os.path.basename(shotgundomainfile)
        shotgunanalysis = './' + shellfile + ' ' + runfile + ' ' + shotgundomain  # gives the command the shell file needs to run
        # subprocess.call([shotgunanalysis], shell=True)
        proc = subprocess.Popen([shotgunanalysis], shell=True, stdout=subprocess.PIPE)
        if os.path.exists(os.path.abspath('log.txt')):
            startstring = open('log.txt', 'wt')
            startstring.write('Shotgun Taxonomy Analysis started \n Command: %s \n' % shotgunanalysis)
            startstring.close()
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line.rstrip(), file=open('log.txt', 'a')) # writes stdout to log
            print(line.rstrip())
        print('Analysis completed succesfully', file=open('log.txt', 'a'))
        for _ in range(3):
            self.rename_resultfolder()
            self.move_result_files()
            self.move_projectfolder()
            self.move_logfile()
            self.rename_placementstree()
            self.rename_violin()
            self.rename_bindigsummary()
            self.rename_bindigmodel()
            self.rename_bindigcluster()
            self.rename_bindingquery()
        #self.move_shotgun_results()  # moves the results fastq files created in shotgun taxonomy analysis to the Projectfolder
        self.move_jobfolder()
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('Shotgun Metagenome-Analysis completed succesfully')
        self.pop_up.open()
        print('Shotgun Taxonomy Analysis finished in ', (time.time() - start_time) / 3600, 'h')
        self.shotgunchecker = self.shotgunchecker + 1

    def reset_shotgundom(self): # resets the bgcmanifestdisplay,bgcmanifestchooser etc., also deletes the imported files to make new analysis possible
        if self.shotgunchecker == 0 or self.shotgunchecker == 3:
            self.set_shotgunchecker_zero()
            self.shotgundommanifestdisplay = ''
            self.shotgundomfastqdisplay = ''
            self.empty_jobname() # empties the jobname file the file
            self.projectname_popup.projectdisplay = ''
            self.delete_files_reset_bgc()
            self.delete_fastq_bgc()
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text("Can't reset during Analysis")
            self.pop_up.open()



    # +++++++++++++++++++++++++++++++++++++++++++
    # CUSTOM PIPELINE RUN FUNCTIONS
    # +++++++++++++++++++++++++++++++++++++++++++


    def check_shell(self): # checks wether shell file was chosen, used mainly in whichrun to run the custom analysis
        try: shell
        except NameError:
            pass
        else:
            return True

    def run_custom(self, filename):  # runs the 16s analysis and updates the sixteens progressbar when finished
        #self.set_sixteenschecker_zero()
        #self.sixteenschecker = self.sixteenschecker + 1
        self.place_manifest(filename)
        thread_pool_executor.submit(self.custom_analysis)

    def custom_analysis(self):
        print('custom_analysis')
        #self.shotgunchecker = self.shotgunchecker + 1
        self.create_projectfolder()
        self.create_pipelinefolder()
        self.get_jobname()
        self.get_pipelinename()
        global customuserpath
        customuserpath = pipestring + '_' + 'mebigeasy'
        global customresultpath  # gives path to view result files even with multiple jobs run
        customresultpath = os.path.abspath(customuserpath)
        start_time = time.time()
        print(start_time)
        shellfile = os.path.basename(shell)
        runfile = os.path.basename(chosenfile)
        customanalysis = './' + shellfile + ' ' + runfile  # gives the command the shell file needs to run
        print(customanalysis)
        proc = subprocess.Popen([customanalysis], shell=True, stdout=subprocess.PIPE)
        if os.path.exists(os.path.abspath('log.txt')):
            startstring = open('log.txt', 'wt')
            startstring.write('Custom Pipeline Analysis started \n Command: %s \n' % customanalysis)
            startstring.close()
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line.rstrip(), file=open('log.txt', 'a'))
            print(line.rstrip())
        print('Analysis completed succesfully', file=open('log.txt', 'a'))

        #self.move_shotgun_results()  # moves the results fastq files created in shotgun taxonomy analysis to the Projectfolder
        self.move_jobfolder()
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('Custom Analysis completed succesfully')
        self.pop_up.open()
        print('Custom Analysis finished in ', (time.time() - start_time) / 3600, 'h')
        self.shotgunchecker = self.shotgunchecker + 1




    # +++++++++++++++++++++++++++++++++++++++++++
    # General Run Functions
    # +++++++++++++++++++++++++++++++++++++++++++

    def move_result_files(self):  # takes the unzipped file with the unknown uuid folder and moves the files to the known uuid folder, gets called by sixteens_progress_bar
        #self.unzip_sixteens()
        newroot = os.path.abspath('%s' % sixteens_name)
        all_files = []  # empty list where the others are combined later
        pdf_files = glob.glob('%s/**/*.pdf' % newroot, recursive=True)  # looks for .pdf files in unknown folder
        html_files = glob.glob('%s/**/*.html' % newroot, recursive=True)
        csv_files = glob.glob('%s/**/*.csv' % newroot, recursive=True)
        png_files = glob.glob('%s/**/data/*.png' % newroot, recursive=True)  # globs only through the data folder, so only real result pngs get moved
        json_files = glob.glob('%s/**/*.jsonp' % newroot, recursive=True)
        tsv_files = glob.glob('%s/**/*.tsv' % newroot, recursive=True)
        for root, dirs, files in os.walk(newroot):  # walks through unknown folder and make lists for every extension
            html_files
            pdf_files
            csv_files
            png_files
            json_files
            tsv_files
        all_files.extend(html_files + pdf_files + csv_files + png_files + json_files + tsv_files)  # combines the lists in one
        for files in all_files:  # extracts paths out of the list
            base = os.path.basename(files) # gives the name of the file (e.g. overview.html)
            if not os.path.isfile(os.path.join(newroot, base)): # checks for the 14 runs if the file was already created, if yes: stops
                shutil.move(files, newroot)  # moves the files to the known uuid folder


    def move_logfile(self): # moves log file to the known uuid, extra because originally in workingdir
        runfolder = os.path.abspath('{0}/{1}'.format(userfolder, sixteens_name)) # path to the sixteens_folder already in the userfolder, unlike newroot in move_result_files
        if os.path.exists(os.path.abspath('log.txt')):
            res1 = os.path.abspath('log.txt')
            shutil.copy(res1, runfolder)

    def move_sixteens_folders(self):
        newroot = os.path.abspath('%s' % sixteens_name)
        previewdir = os.path.abspath('Preview')
        all_folders = []
        dist_folder = glob.glob('%s/**/data/*dist' % newroot, recursive=True)
        q2templateassets_folder = glob.glob('%s/**/data/*q2templateassets' % newroot, recursive=True)
        css_folder = glob.glob('%s/**/data/*css' % newroot, recursive=True)
        img_folder = glob.glob('%s/**/data/*img' % newroot, recursive=True)
        js_folder = glob.glob('%s/**/data/*js' % newroot, recursive=True)
        templates_folder = glob.glob('%s/**/data/*templates' % newroot, recursive=True)
        vendor_folder = glob.glob('%s/**/data/*vendor' % newroot, recursive=True)
        for root, dirs, files in os.walk(newroot):
            dist_folder
            q2templateassets_folder
            css_folder
            img_folder
            js_folder
            templates_folder
            vendor_folder
        all_folders.extend(dist_folder + q2templateassets_folder + img_folder + templates_folder + vendor_folder + css_folder + js_folder)
        for folders in all_folders:
            base = os.path.basename(folders)  # gives the name of the folder (e.g. overview.html)
            if not os.path.isfile(os.path.join(newroot,base)):  # checks for the 14 runs if the folder was already created, if yes: stops
                shutil.move(folders, newroot)  # moves the folders to the known uuid folder

    def move_projects_to_dir(self):  # moves all projectfiles in Projectfolder
        workingdir = os.path.abspath('')
        projectdir = os.path.abspath('Projects')
        allprojects = glob.glob('%s/*_mebigeasy' % workingdir)
        for root, dirs, files in os.walk(workingdir):
            allprojects
        for folders in allprojects:
            shutil.move(folders, projectdir)


    def unzip_sixteens(self):  # unzips all .qzv files present in the working dir and creates a new folder which has the same name as the .qzv file and contains the uuid folder containig the result files
        rootpath = os.path.abspath('')  # empty because /GUI is the current directory
        pattern = '*.qzv'
        for root, dirs, files in os.walk(rootpath):
            for file_name in fnmatch.filter(files, pattern):
                zipfile.ZipFile(os.path.join(root, file_name)).extractall(os.path.join(root, os.path.splitext(file_name)[0]))
        #for _ in range(14): # runs the function 14 times, once for every possible foldername and creates sixteens folders for all of them
         #   self.rename_sixteens()

    def get_jobname(self): # gives first part of the result_folder (= projectname)
        with open('projectname.txt') as projectnamer:  # gets the string from .txt file and makes it useable
            for projectname in projectnamer:
                self.projectname = projectname.rstrip()
        global jobstring
        jobstring = self.projectname

    def get_pipelinename(self):
        with open('pipelinename.txt') as pipelinenamer:  # gets the string from .txt file and makes it useable
            for pipelinename in pipelinenamer:
                self.pipelinename = pipelinename.rstrip()
        global pipestring
        pipestring = self.pipelinename


    def rename_resultfolder(self):  # renames the gui created result folder and gives it a uuid which we can access when we display the results
        try: chosenfile
        except NameError:
            try: chosenresult
            except NameError:
                try: bgcfile
                except NameError:
                    filepath = os.path.abspath(shotgundomainfile)
                else:
                    filepath = os.path.abspath(bgcfile)
        else:
            filepath = os.path.abspath(chosenfile)
        #global projectstring
        #projectstring = self.projectname # gives the user defined project name
        global startstring # needed when renaming the index files
        startstring = uuid.uuid4().hex # gives uuid
        if os.path.exists(os.path.abspath('paired-end-demux')):
            foldername = os.path.abspath('paired-end-demux')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('rep-seqs')):
            foldername = os.path.abspath('rep-seqs')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('alpha-rarefaction')):
            foldername = os.path.abspath('alpha-rarefaction')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('table')):
            foldername = os.path.abspath('table')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('taxa-bar-plots')):
            foldername = os.path.abspath('taxa-bar-plots')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('taxonomy')):
            foldername = os.path.abspath('taxonomy')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/bray_curtis_emperor')):
            foldername = os.path.abspath('core-metrics-results/bray_curtis_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('bray_curtis_emperor')): # both necessary because if result run, the core-metrics-folder doesnt exist
            foldername = os.path.abspath('bray_curtis_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/evenness-group-significance')):
            foldername = os.path.abspath('core-metrics-results/evenness-group-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('evenness-group-significance')):
            foldername = os.path.abspath('evenness-group-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/faith-pd-group-significance')):
            foldername = os.path.abspath('core-metrics-results/faith-pd-group-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('faith-pd-group-significance')):
            foldername = os.path.abspath('faith-pd-group-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/jaccard_emperor')):
            foldername = os.path.abspath('core-metrics-results/jaccard_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('jaccard_emperor')):
            foldername = os.path.abspath('jaccard_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/unweighted_unifrac_emperor')):
            foldername = os.path.abspath('core-metrics-results/unweighted_unifrac_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('unweighted_unifrac_emperor')):
            foldername = os.path.abspath('unweighted_unifrac_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/unweighted-unifrac-site-significance')):
            foldername = os.path.abspath('core-metrics-results/unweighted-unifrac-site-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('unweighted-unifrac-site-significance')):
            foldername = os.path.abspath('unweighted-unifrac-site-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/unweighted-unifrac-layer-significance')):
            foldername = os.path.abspath('core-metrics-results/unweighted-unifrac-layer-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('unweighted-unifrac-layer-significance')):
            foldername = os.path.abspath('unweighted-unifrac-layer-significance')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('core-metrics-results/weighted_unifrac_emperor')):
            foldername = os.path.abspath('core-metrics-results/weighted_unifrac_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('weighted_unifrac_emperor')):
            foldername = os.path.abspath('weighted_unifrac_emperor')
            endstring = '16s_mebig'
        if os.path.exists(os.path.abspath('denoising-stats')):  # last 16s folder
            foldername = os.path.abspath('denoising-stats')
            endstring = '16s_mebig'
        try: namer1
        except NameError: pass
        else:
            if os.path.exists(os.path.abspath('%s.bigmex_dom_div_AMP-binding' % namer1)): # first bgc folder
                foldername = os.path.abspath('%s.bigmex_dom_div_AMP-binding' % namer1)
                endstring = 'bgc_mebig' # different endstring for bgc runs
        try: namer2
        except NameError: pass
        else:
            if os.path.exists(os.path.abspath('%s.bigmex_dom_div_AMP-binding' % namer2)):
                foldername = os.path.abspath('%s.bigmex_dom_div_AMP-binding' % namer2)
                endstring = 'bgc_mebig'
        if os.path.exists(os.path.abspath('out_dom_merged_div_AMP-binding')):
            foldername = os.path.abspath('out_dom_merged_div_AMP-binding')
            endstring = 'bgc_mebig'
        try: foldername
        except NameError: pass
        else:
            runstring = os.path.splitext(os.path.basename(foldername)) [0] # gives .qzv name that exists in working dir
            global sixteens_name # names the new run folder
            #sixteens_name = projectstring + '_' + runstring + '_' + startstring + endstring  # gives run folder name
            sixteens_name = jobstring + '_' + runstring + '_' + startstring + endstring  # gives run folder name
            newroot = os.path.abspath('%s' % sixteens_name)  # gives path to the sixteens folder (= result folder)
            os.rename(foldername, '%s' % sixteens_name)
            if os.path.exists(os.path.abspath('%s.qzv' % foldername)):  # moves the qzv-file of the 16s run to the result folder
                shutil.move('%s.qzv' % foldername, newroot)

    def move_shotgun_results(self): # moves the results fastq files created in shotgun taxonomy analysis to the Projectfolder
        if os.path.exists(os.path.abspath('%s.r1andr2reads.fastq.gz' % namer1)):
            res1 = os.path.abspath('%s.r1andr2reads.fastq.gz' % namer1)
            shutil.move(res1, userfolder)
        if os.path.exists(os.path.abspath('%s.r1andr2reads.fastq.gz' % namer2)):
            res1 = os.path.abspath('%s.r1andr2reads.fastq.gz' % namer2)
            shutil.move(res1, userfolder)
        if os.path.exists(os.path.abspath('log.txt')):
            res1 = os.path.abspath('log.txt')
            shutil.copy(res1, userfolder)



    def place_manifest(self):  # takes the manifest file of the user and places it in the working directory, then runs the Analysis
        #file = '%s' % filename[0]  # manifest-data file gets chosen
        all_files = []
        if self.check_display_sixteens() is True:
            chosenbase = os.path.basename(sixteensmanifest)  # file name of chosefile, needed if the users manifest-file has a space
            chosenpath = os.path.dirname(sixteensmanifest)  # gives path of manifest-data file, because fastq files need to be saved in same directory
        if self.check_display_bgc() is True:
            chosenbase = os.path.basename(bgcmanifest)  # file name of chosefile, needed if the users manifest-file has a space
            chosenpath = os.path.dirname(bgcmanifest)  # gives path of manifest-data file, because fastq files need to be saved in same directory
        if self.check_display_shotguntax() is True:
            chosenbase = os.path.basename(shotguntaxmanifest)  # file name of chosefile, needed if the users manifest-file has a space
            chosenpath = os.path.dirname(shotguntaxmanifest)  # gives path of manifest-data file, because fastq files need to be saved in same directory
        if self.check_display_shotguntax() is True:
            chosenbase = os.path.basename(shotguntaxmanifest)  # file name of chosefile, needed if the users manifest-file has a space
            chosenpath = os.path.dirname(shotguntaxmanifest)  # gives path of manifest-data file, because fastq files need to be saved in same directory
        if self.check_display_shotgundom () is True:
            chosenbase = os.path.basename(shotgundommanifest)  # file name of chosefile, needed if the users manifest-file has a space
            chosenpath = os.path.dirname(shotgundommanifest)  # gives path of manifest-data file, because fastq files need to be saved in same directory
        #fastqfiles = glob.glob('%s/*.gz' % chosenpath, recursive=True)  # looks for fastq files in directory
        #metadatafile = glob.glob('%s/*.tsv' % chosenpath, recursive=True)
        workingdir = os.path.abspath('')  # empty because GUI is the current directory
        global nospacemanifest
        nospacemanifest = os.path.join(workingdir, chosenbase)  # path for chosen file in working directory
        if chosenpath != workingdir:  # happens only if manifest and fastq files arent already available in the working directory
            '''for root, dirs, files in os.walk(chosenpath):  # walks through directory and collects the fastq and metadata files in a list
                fastqfiles
                #metadatafile
            all_files.extend(fastqfiles)
            for files in all_files:  # extracts the paths of the files from the list
                shutil.copy(files, workingdir)  # copies fastqfiles to working directory'''
            if self.check_display_sixteens() is True:
                firstfile = shutil.copy(sixteensmanifest, workingdir)  # copies manifest-data file to working directory
            if self.check_display_bgc() is True:
                firstfile = shutil.copy(bgcmanifest, workingdir)  # copies manifest-data file to working directory
            if self.check_display_shotguntax() is True:
                firstfile = shutil.copy(shotguntaxmanifest, workingdir)  # copies manifest-data file to working directory
            if self.check_display_shotgundom() is True:
                firstfile = shutil.copy(shotgundommanifest, workingdir)  # copies manifest-data file to working directory
            nospacemanifest = nospacemanifest.replace(' ', '-')  # now that the manifest data file was copied to the working directory, the space is replaced (if that would happen earlier, it would remove every space in the path and crash)
            if nospacemanifest != firstfile:
                shutil.copy(firstfile, nospacemanifest)  # exchanges the space file with the non-space file
                os.remove(firstfile)  # removes the file containing the space

    def place_metadata(self): # s.place_manifest
        workingdir = os.path.abspath('')
        chosenmetadata = os.path.basename(metadata) # metadata gets defined in get_sixteenmetadata
        chosenpath = os.path.dirname(metadata)
        nospacemetadata = os.path.join(workingdir, chosenmetadata)
        if chosenpath != workingdir:
            firstfile = shutil.copy(metadata, workingdir)
        nospacemetadata = nospacemetadata.replace(' ', '-')
        if nospacemetadata != firstfile:
            shutil.copy(firstfile, nospacemetadata)
            os.remove(firstfile)

    def place_fastq(self): # s.place_manifest
        workingdir = os.path.abspath('')
        if self.check_display_sixteens() is True:
            chosenpath = os.path.dirname(fastqfiles[0])
            if chosenpath != workingdir:
                for files in fastqfiles:
                    shutil.copy(files, workingdir)
        if self.check_display_bgc() is True:
            chosenpath = os.path.dirname(bgcfastqfiles[0])
            if chosenpath != workingdir:
                for files in bgcfastqfiles:
                    shutil.copy(files, workingdir)
        if self.check_display_shotguntax() is True:
            chosenpath = os.path.dirname(shotguntaxfastqfiles[0])
            if chosenpath != workingdir:
                for files in shotguntaxfastqfiles:
                    shutil.copy(files, workingdir)
        if self.check_display_shotgundom() is True:
            chosenpath = os.path.dirname(shotgundomfastqfiles[0])
            if chosenpath != workingdir:
                for files in shotgundomfastqfiles:
                    shutil.copy(files, workingdir)





    def place_result(self, filename):  # takes .qzv file from any given dir and places it in working dir (s. place_manifest)
        file = '%s' % filename[0]
        chosenpath = os.path.dirname(file)
        workingdir = os.path.abspath('')
        if chosenpath != workingdir:
            shutil.copy(file, workingdir)

    def delete_files(self):  # deletes variety of files and folders that are moved or created to/in the working directory while  analyzing
        remove_files = []
        remove_folders = []
        workingdir = os.path.abspath('')
        if self.check_sixteens() is True:
            uuidfile = os.path.abspath('%s' % sixteens_name)
            #workingdir = os.path.dirname(uuidfile)  # gives the path of the directory of the uuid file which is the same for the other files as well, so now we have the path for all file types
        #if self.check_domainname() or self.check_sixteens()  is True:
        if self.check_project() is True:
            userfile = os.path.abspath(userfolder)
        else: pass
        bigmexfolder = glob.glob('%s/*BiG-MEx' % workingdir, recursive=True)
        fastqfiles = glob.glob('%s/*.gz' % workingdir, recursive=True)  # looks for fastq files in directory
        qzvfiles = glob.glob('%s/*.qzv' % workingdir, recursive=True)
        qzafiles = glob.glob('%s/*.qza' % workingdir, recursive=True)
        metadatafiles = glob.glob('%s/*.tsv' % workingdir, recursive=True)
        logfiles =glob.glob('%s/*.log' % workingdir, recursive=True)
        alluserfiles = glob.glob('%s/*mebigeasy' % workingdir, recursive=True)  # looks for userfolders files in directory (has no effect on folders in 'Projects'
        sixteensfile = os.path.abspath('sixteensname.txt')
        bgchelpfiles = glob.glob('%s/**/*annot' % workingdir, recursive=True)
        pngfiles =  glob.glob('%s/Preview/*.png' % workingdir, recursive=True) # looks for png files moved to preview dir to create preview files
        csvfiles = glob.glob('%s/Preview/*.csv' % workingdir, recursive=True) # looks for csv files moved to preview dir to create preview files
        #sixteenspreview = glob.glob('%s/Preview/sixteenspreview.html' % workingdir,recursive=True)  # looks for 'used' sixteenspreview.html to delete it, because new sixteenspreview.html gets copied to 'Preview'
        for files in os.walk(workingdir):
            qzvfiles
            qzafiles
            fastqfiles
            metadatafiles
            logfiles
            alluserfiles
            pngfiles
            csvfiles
            #sixteenspreview
        remove_files.extend(qzvfiles + qzafiles + fastqfiles + alluserfiles + metadatafiles + logfiles + pngfiles + csvfiles)
        for files in remove_files:
            if not files.endswith('silva-132-99-nb-classifier.qza'): # crucial for taxonomy analysis, needs to be present in working directory!
                os.remove(files)

        for folders in os.walk(workingdir): # seperate because special command to delete folders
            #alluuidfiles
            #alluserfiles
            bgchelpfiles
            bigmexfolder
        remove_folders.extend(bgchelpfiles + bigmexfolder)
        for folders in remove_folders:
            shutil.rmtree(folders)
        '''for alluuidfiles in alluuidfiles:  # removes uuid folders from older runs
            shutil.rmtree(alluuidfiles)  # when removing folders use this command, otherwise no permission to work with folder
        for alluserfiles in alluserfiles:
            shutil.rmtree(alluserfiles)
        for bgchelpfiles in bgchelpfiles:
            shutil.rmtree(bgchelpfiles)
        for bigmexfolder in bigmexfolder:
            shutil.rmtree(bigmexfolder)'''
        if self.check_project() is True:
            if os.path.exists(userfile):
                shutil.rmtree(userfile)
        if os.path.exists(sixteensfile):
            os.remove(sixteensfile)

    def delete_files_reset_sixteens(self):
        remove_files = []
        remove_folders = []
        workingdir = os.path.abspath('')
        if self.check_manifest_sixteens() is True and self.check_metadata_sixteens() is True:
            manifestfile = os.path.join(workingdir, os.path.basename(os.path.abspath(sixteensmanifest)))
            metadatafile = os.path.join(workingdir, os.path.basename(os.path.abspath(metadata)))
            if os.path.exists(manifestfile):
                os.remove(manifestfile)
            if os.path.exists(metadatafile):
                os.remove(metadatafile)

        qzvfiles = glob.glob('%s/*.qzv' % workingdir, recursive=True)
        qzafiles = glob.glob('%s/*.qza' % workingdir, recursive=True)
        for files in os.walk(workingdir):
            qzvfiles
            qzafiles
        remove_files.extend(qzvfiles + qzafiles)
        for files in remove_files:
            if not files.endswith('silva-132-99-nb-classifier.qza'):  # crucial for taxonomy analysis, needs to be present in working directory!
                os.remove(files)

    def delete_fastq_sixteens(self):
        workingdir = os.path.abspath('')
        try: fastqfiles
        except NameError:
            pass
        else:
            dirname = fastqfiles[0]
            dirlength = len(os.path.dirname((dirname)))  # necessary to get len of path til fastq files
            fastqbases = []  # list which will contain bases
            for z in fastqfiles:
                fastqbases.append(z[dirlength + 1:]) # only the bases, removes the / before fastqfile
            workingfastq = [workingdir + '/' + s for s in fastqbases]
            if os.path.exists(os.path.abspath(workingfastq[0])):
                for files in workingfastq:
                    os.remove(files)

    def delete_files_reset_bgc(self):
        remove_files = []
        remove_folders = []
        workingdir = os.path.abspath('')
        bigmexfolder = glob.glob('%s/*BiG-MEx' % workingdir, recursive=True)
        bgchelpfiles = glob.glob('%s/**/*annot' % workingdir, recursive=True)
        if self.check_manifest_bgc() is True:
            manifestfile = os.path.join(workingdir, os.path.basename(os.path.abspath(bgcmanifest)))
        if self.check_manifest_shotgundom() is True:
            manifestfile = os.path.join(workingdir, os.path.basename(os.path.abspath(shotgundommanifest)))
            if os.path.exists(manifestfile):
                os.remove(manifestfile)

        for folders in os.walk(workingdir):  # seperate because special command to delete folders
            bgchelpfiles
            bigmexfolder
        remove_folders.extend(bgchelpfiles + bigmexfolder)
        for folders in remove_folders:
            shutil.rmtree(folders)

    def delete_fastq_bgc(self):
        workingdir = os.path.abspath('')
        try: bgcfastqfiles
        except NameError:
            try: shotgundomfastqfiles
            except NameError: pass
            else:
                dirname = shotgundomfastqfiles[0]
        else:
            dirname = bgcfastqfiles[0]
        dirlength = len(os.path.dirname((dirname)))  # necessary to get len of path til fastq files
        fastqbases = []  # list which will contain bases
        for z in shotgundomfastqfiles:
            fastqbases.append(z[dirlength + 1:]) # only the bases
        workingfastq = [workingdir + '/' + s for s in fastqbases]
        if os.path.exists(os.path.abspath(workingfastq[0])):
            for files in workingfastq:
                os.remove(files)

    def delete_files_reset_shotguntax(self):
        remove_files = []
        remove_folders = []
        workingdir = os.path.abspath('')
        if self.check_manifest_sixteens() is True and self.check_metadata_sixteens() is True:
            manifestfile = os.path.join(workingdir, os.path.basename(os.path.abspath(shotguntaxmanifest)))
            if os.path.exists(manifestfile):
                os.remove(manifestfile)

    def delete_fastq_shotguntax(self):
        workingdir = os.path.abspath('')
        try: shotguntaxfastqfiles
        except NameError: pass
        else:
            dirname = shotguntaxfastqfiles[0]
            dirlength = len(os.path.dirname((dirname)))  # necessary to get len of path til fastq files
            fastqbases = []  # list which will contain bases
            for z in shotguntaxfastqfiles:
                fastqbases.append(z[dirlength + 1:]) # only the bases
            workingfastq = [workingdir + '/' + s for s in fastqbases]
            if os.path.exists(os.path.abspath(workingfastq[0])):
                for files in workingfastq:
                    os.remove(files)




    def delete_preview_png(self): # for preview html files pngs are moved to preview dir, they have to be deleted when starting new analysis, so there arent multiple results with the same name in dir
        previewdir = os.path.abspath('Preview')
        pngfiles = glob.glob('%s/*.png' % previewdir, recursive=True)  # looks for png files moved to preview dir to create preview files
        for files in os.walk(previewdir):
            pngfiles
        for files in pngfiles:
            os.remove(files)

    def delete_sixteensshell(self): # after every one old sixteens shell gets deleted, so a new one can be moved to working dir
        shell = os.path.abspath('16Spipeline_qiime2v2019v4docker_gui_v1.sh')
        os.remove(shell)

    def delete_configfile(self):
        config = os.path.abspath('config-file.txt')
        os.remove(config)



    def delete_manifest_sixteens(self):  # deletes the manifest file (outsourced from delete_sixteens to improve readability)
        try:
            usermanifest  # only if usermanifest was created (so only if Analysis was run) do the if clause
        except NameError:
            pass
        else:
            if os.path.isfile(os.path.abspath(usermanifest)):  # removes manifest-data file if it exists
                os.remove(os.path.abspath(usermanifest))
        try:
            nospacemanifest
        except NameError:
            pass
        else:
            if os.path.isfile(nospacemanifest):  # removes manifest-data file containing a space if it exists
                os.remove(nospacemanifest)


    def check_sixteens(self):  # checks if sixteens_name was defined (by that checks if analysis was run), if no tells user to analyze via popup
        try:
            sixteens_name
        except NameError:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('Please run Analysis first')
            self.pop_up.open()
        else:
            return True

    def change_shell_manifest(self):  # soft codes the shell script for any given manifest or sample-metadata file with the name of choice by user
        shellfile = os.path.abspath('16Spipeline_qiime2v2019v4docker_gui_v1.sh')

        '''metapath = os.path.dirname(os.path.abspath(manifest))
        metadatafile = glob.glob('%s/*.tsv' % metapath)
        for files in os.walk(metapath):
            metadatafile
        for metadata in metadatafile:
            metadata'''
        global usermanifest
        usermanifest = os.path.basename(sixteensmanifest)
        usermanifest = usermanifest.replace(' ', '-')  # changes space to minus in the manifest data file name
        '''global usermeta
        usermeta = os.path.basename(metadata)
        usermeta = usermeta.replace(' ', '-')'''
        a = open(shellfile, 'rt')  # opens file in read text mode
        data = a.read()  # reads whole text to variable data
        data = data.replace('manifest-data', usermanifest)  # replaces all occurences of manifest-data with newstring
        #data = data.replace('sample-metadata.tsv', usermeta)
        a.close()  # closes input file
        a = open(shellfile, 'wt')  # opens shellfile in write text mode
        a.write(data)  # writes data to shellfile
        a.close()  # closes shellfile

    def change_shell_metadata(self): # s.change_manifest
        shellfile = os.path.abspath('16Spipeline_qiime2v2019v4docker_gui_v1.sh')
        global usermetadata
        usermetadata = os.path.basename(metadata)
        usermetadata = usermetadata.replace(' ', '-')  # changes space to minus in the manifest data file name
        a = open(shellfile, 'rt')  # opens file in read text mode
        data = a.read()  # reads whole text to variable data
        data = data.replace('sample-metadata.tsv', usermetadata)
        a.close()  # closes input file
        a = open(shellfile, 'wt')  # opens shellfile in write text mode
        a.write(data)  # writes data to shellfile
        a.close()  # closes shellfile



    def undo_change_shell(self):  # sets shell file back to default after Analysis is completed(manifest-data, configs), makes multiple analyzations possible
        try:
            usermanifest
            usermetadata
        except NameError:
            pass
        else:
            shellfile = os.path.abspath('16Spipeline_qiime2v2019v4docker_gui_v1.sh')
            a = open(shellfile, 'rt')
            data = a.read()
            data = data.replace(usermanifest, 'manifest-data')
            data = data.replace(usermetadata, 'sample-metadata.tsv')
            data = data.replace(no1, ' --p-trim-left-f 0')
            data = data.replace(no2, ' --p-trim-left-r 0')
            data = data.replace(no3, ' --p-trunc-len-f 300')
            data = data.replace(no4, ' --p-trunc-len-r 300')
            data = data.replace(no5, ' --p-sampling-depth 1500')
            data = data.replace(no6, ' --p-max-depth 4000')
            a.close()

            a = open(shellfile, 'wt')
            a.write(data)
            a.close()

    def check_result(self): # if the result file doesnt exist, opens popup telling the user to analyse
        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('This file does not exist, run Analysis first')
        self.pop_up.open()

    def create_projectfolder(self): # creates folder in working dir with user-given projectname
        dirpath = os.path.abspath('') # gives absolute path for working directory
        with open('projectname.txt') as fobj:
            for projectname in fobj:
                self.projectname = projectname.rstrip()
        global userfolder
        userfolder = self.projectname
        global folderpath
        folderpath = os.path.abspath(userfolder) # gives the path of the unique userfolder, mainly used in result functions to glob through entire directoy for making earlier runs viewable
        if not os.path.exists(os.path.abspath(folderpath)):
            os.mkdir('%s' % userfolder)
        else:
            pass

    def create_pipelinefolder(self): # s. create_projectname
        dirpath = os.path.abspath('') # gives absolute path for working directory
        with open('pipelinename.txt') as fobj:
            for pipelinename in fobj:
                self.pipelinename = pipelinename.rstrip()
        global pipelinefolder
        pipelinefolder = self.pipelinename + '_' + 'mebigeasy'
        global pipelinepath
        pipelinepath = os.path.abspath(pipelinefolder) # gives the path of the unique userfolder, mainly used in result functions to glob through entire directoy for making earlier runs viewable
        if not os.path.exists(os.path.abspath(pipelinepath)):
            os.mkdir('%s' % pipelinefolder)
        else:
            pass


    def move_projectfolder(self): # puts the sixteens_name folder in the project folder
        # src = os.path.abspath('%s' % sixteens_name)
        workingdir = os.path.abspath('')
        sixteensmebigfolder = glob.glob('%s/*mebig' % workingdir) # globs for all folders created by rename_resultfolder
        bgcmebigfolder = glob.glob('%s/*mebig' % workingdir) # globs for all folders created by rename_resultfolder
        dst = os.path.abspath(('%s' % userfolder))
        for root, dirs, files in os.walk(workingdir):
            sixteensmebigfolder
        for folders in sixteensmebigfolder:
            shutil.move(folders, dst) # moves the mebigfolders in projectfolder

    def move_jobfolder(self): # moves jobfolder in projectfolder, own function because should happen at a single event at the end of analysis
        shutil.move(folderpath, pipelinepath)



    def fill_projectfolder(self, symlinks = False, ignore = None): # copies the content of the uuid folder into the project folder
        src = os.path.abspath('%s' % sixteens_name)
        dst = os.path.abspath(('%s' % userfolder))
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def check_project(self): # checks wether new data can be imported, only the case if userfolder exists
        try:
            userfolder
        except NameError:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('Before Importing Data, start a new Project')
            self.pop_up.open()
        else:
            return True


    def rename_index(self): # renames if created during run the index.html to make it unique for the ran qzv file
        html_file = os.path.abspath('{0}/{1}/index.html'.format(jobstring, sixteens_name)) # gives index file to rename
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name)) # gives "result" directory" where file gets copied to from working directory
        #filestring = os.path.splitext(os.path.basename(html_file))[0] # gives string 'index'
        filepath = os.path.abspath(dir) # gives path of run file
        runstring = os.path.splitext(os.path.basename(filepath))[0]  # gives .qzv or manifest file string that was run
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('16s_mebig', '')
        c = b.replace('%s' % startstring, '') # finally, just the string part which gives the qzv name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'index' + '.html' # creates new unique index file name
        if os.path.isfile(html_file):
            newindex = os.rename(html_file, finalfile)
            newindex
            showindex = os.path.abspath(finalfile) # gives working dir
            shutil.move(showindex, dir) # moves the unique index to result dir

    def rename_permanovapairwise(self): # s. rename_index
        csv_file = os.path.abspath('{0}/{1}/permanova-pairwise.csv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        #filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('16s_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'permanova-pairwise' + '.csv'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newperma = os.rename(csv_file, finalfile)
            newperma
            showindex = os.path.abspath(finalfile)

            shutil.move(showindex, dir)

    def rename_kruskallayer(self): # renames kruskal-wallis-pairwise-Layer like in rename_index
        csv_file = os.path.abspath('{0}/{1}/kruskal-wallis-pairwise-Layer.csv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('16s_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'kruskal-wallis-pairwise-Layer' + '.csv'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newlayer = os.rename(csv_file, finalfile)
            newlayer
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def rename_kruskalsite(self): # renames kruskal-wallis-pairwise-Site like in rename_index
        csv_file = os.path.abspath('{0}/{1}/kruskal-wallis-pairwise-Site.csv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('16s_mebig', '')
        c = b.replace('%s' % startstring, '')
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'kruskal-wallis-pairwise-Site' + '.csv'
        if os.path.isfile(csv_file):
            newsite = os.rename(csv_file, finalfile)
            newsite
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def rename_metadata(self): # s. rename_index
        csv_file = os.path.abspath('{0}/{1}/metadata.tsv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        #filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('16s_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'metadata' + '.tsv'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newperma = os.rename(csv_file, finalfile)
            newperma
            showindex = os.path.abspath(finalfile)

            shutil.move(showindex, dir)

    def rename_placementstree(self): # renames placementtree of BGC Amplicon pipeline like in rename_index
        csv_file = os.path.abspath('{0}/{1}/AMP-binding_placements_tree.pdf'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('bgc_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the qzv name
        d = c.replace('%s_' % jobstring, '')  # finally, just the string part which gives the result name
        namestring = d.replace('%s_' % jobstring, '')
        finalfile = namestring + 'AMP-binding_placements_tree' + '.pdf'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newlayer = os.rename(csv_file, finalfile)
            newlayer
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def rename_violin(self): # renames violin of BGC Amplicon pipeline like in rename_index
        csv_file = os.path.abspath('{0}/{1}/AMP-binding_violin_div_est.pdf'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('bgc_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'AMP-binding_violin_div_est' + '.pdf'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newlayer = os.rename(csv_file, finalfile)
            newlayer
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def rename_bindigmodel(self): # renames result of BGC Amplicon pipeline like in rename_index
        csv_file = os.path.abspath('{0}/{1}/AMP-binding_model_div_est.tsv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('bgc_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'AMP-binding_model_div_est' + '.tsv'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newlayer = os.rename(csv_file, finalfile)
            newlayer
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def rename_bindigsummary(self): # renames result of BGC Amplicon pipeline like in rename_index
        csv_file = os.path.abspath('{0}/{1}/AMP-binding_summary_model_div_est.tsv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('bgc_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'AMP-binding_summary_model_div_est' + '.tsv'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newlayer = os.rename(csv_file, finalfile)
            newlayer
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def rename_bindigcluster(self): # renames result of BGC Amplicon pipeline like in rename_index
        csv_file = os.path.abspath('{0}/{1}/AMP-binding_cluster2abund.tsv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('bgc_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'AMP-binding_cluster2abund' + '.tsv'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newlayer = os.rename(csv_file, finalfile)
            newlayer
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def rename_bindingquery(self): # renames result of BGC Amplicon pipeline like in rename_index
        csv_file = os.path.abspath('{0}/{1}/AMP-binding_query_info.csv'.format(jobstring, sixteens_name))
        dir = os.path.dirname('{0}/{1}/'.format(jobstring, sixteens_name))
        filestring = os.path.splitext(os.path.basename(csv_file))[0]
        filepath = os.path.abspath(dir)
        runstring = os.path.splitext(os.path.basename(filepath))[0]
        a = runstring.replace('%s_' % runstring, '')
        b = a.replace('bgc_mebig', '')
        c = b.replace('%s' % startstring, '')  # finally, just the string part which gives the result name
        namestring = c.replace('%s_' % jobstring, '')
        finalfile = namestring + 'AMP-binding_query_info' + '.csv'  # creates new unique index file name
        if os.path.isfile(csv_file):
            newlayer = os.rename(csv_file, finalfile)
            newlayer
            showindex = os.path.abspath(finalfile)
            shutil.move(showindex, dir)

    def path_importfiles(self): # gets the User path for Importchooser
        if sys.platform == 'darwin':  # for MacOs
            username = getpass.getuser()
            for root, dirs, files in os.walk("/"):
                for name in dirs:
                    if name == 'Users':
                        p = root + name + '/' + username + '/' + 'Documents'
                        return p
        if sys.platform in ["linux", "linux2"]: # for Linux
            for root, dirs, files in os.walk('/'):
                for name in dirs:
                    if name == username:
                        p = root + username
                        return p
        else: # for windows
            p = root
            return p

    def get_domainname(self, value): # gives user-chosen domainname for BGC Amplicon Analysis
        global domainname
        if value == 'PKS-KS':
            domainname = 'PKS_KS'
        if value == 'AMP-binding':
            domainname = 'AMP-binding'
        if value == 'Type-2 KS':
            domainname = 't2ks'
        if value == 'Domain Name':
            domainname = 'domainname'
        print(domainname, 'Domainname')

    def get_domainname_shotgun(self, value): # gives user-chosen domainname for shotgun meta domain profiling
        global shotgundomain
        shotgundomain = value
        print(shotgundomain, 'Shotgun-Domainname')

    def check_shotgundomain(self):
        try:
            shotgundomain
        except NameError:
            pass
        else:
            return True


    def delete_manifest_bgc(self):
        try:
            bgcbase
        except NameError:
            pass
        else:
            if os.path.isfile(os.path.abspath(bgcbase)):  # removes manifest-data file if it exists
                os.remove(os.path.abspath(bgcbase))


    def check_domainname(self): # tests for domainname variable, used in whichrun_sixteens to decide which pipeline is run
        try:
            domainname
        except NameError:
            pass
        else:
            return True


    def domainname_amp(self): # is used in the result functions to decide on which domainname the analysis was run, and which result should be opened according to that
        if self.check_domainname() is True:
            if domainname == 'AMP-binding':
                return True
            else: return False

    def domainname_pks(self): # s. domainname_amp
        if self.check_domainname() is True:
            if domainname == 'PKS_KS':
                return True
            else: return False

    def domainname_t2ks(self):# s. domainname_amp
        if self.check_domainname() is True:
            if domainname == 't2ks':
                return True
            else: return False

    def domainname_domainname(self): # used to check wether a real domainname was chosen or not
        if self.check_domainname() is True:
            if domainname == 'domainname':
                return True
            else: return False

    def shotgundomain_domainname(self):
        if self.forbid_shotguntaxprofiling() is True:
            if shotgundomain == 'Domain Name':
                return True
            else:
                return False

    def forbid_sixteens(self): # forbids whichrun to run 16sAnalysis when a real domainname is chosen in the spinner
        if self.domainname_amp() is True or self.domainname_pks() is True or self.domainname_t2ks() is True:
            return True
        else: return False

    def forbid_shotguntaxprofiling(self): # decides wether shotgun tax or domain profiling is run
        try: shotgundomain
        except NameError:
            return False
        else:
            if shotgundomain == 'Domain Name': # if shotgundomain is 'domainname', shotgun tax profiling should run
                return False
            else:
                return True

    def do_nothing(self): # when deciding which result popup to open, this function works like else: pass
        pass


    def get_namers(self): # gives names for the result files in bgc because they get created according to user built manifest file
        list1 = []
        str = ''
        if self.check_bgcfile() is True:
            print('True, bgcfile')
            x = open(os.path.abspath(bgcfile), 'r')
        elif self.check_shotguntaxfile() is True:
            print('True, check_shotguntaxfile')
            x = open(os.path.abspath(shotguntaxfile), 'r')
        else:
            x = open(os.path.abspath(shotgundomainfile), 'r')
        a = x.readlines()
        firstcol = a[0] # gives first col of bgc manifest
        secondcol = a[1] # gives second col of bgc manifest
        firstsplit = firstcol.split(' ', 1)
        namer1list = [firstsplit[0]]
        global namer1 # gives string of the name of the first (nr1) created folder (the name of the first column in bgc manifest file)
        namer1 = str.join(namer1list)
        secondsplit = secondcol.split(' ', 1)
        namer2list = [secondsplit[0]]
        global namer2  # gives string of the name of the second (nr2) created folder (the name of the second column in bgc manifest file)
        namer2 = str.join(namer2list)
        print(namer1)
        print(namer2)

    def check_namer1(self):
        try: namer1
        except NameError: pass
        else: return True


    def check_bgcfile(self):
        try: bgcfile
        except NameError:
            pass
        else:
            return True

    def check_shotguntaxfile(self):
        try: shotguntaxfile
        except NameError:
            pass
        else:
            return True

    def check_shotgundomainfile(self):
        try: shotgundomainfile
        except NameError:
            pass
        else:
            return True

    def check_sixteenslogtext(self): # check if log-file exists
        if os.path.exists(os.path.abspath('log.txt')):
            return True
        else:
            return False

    def empty_logtext(self):
        #raw = open('log.txt', 'bgclog.txt', 'shotguntax.txt', 'r+')
        raw = open('log.txt', 'r+')
        raw.read().split("\n")
        raw.seek(0)
        raw.truncate()

    def empty_pipelinename(self):
        #raw = open('log.txt', 'bgclog.txt', 'shotguntax.txt', 'r+')
        raw = open('pipelinename.txt', 'r+')
        raw.read().split("\n")
        raw.seek(0)
        raw.truncate()

    def empty_jobname(self):
        #raw = open('log.txt', 'bgclog.txt', 'shotguntax.txt', 'r+')
        raw = open('projectname.txt', 'r+')
        raw.read().split("\n")
        raw.seek(0)
        raw.truncate()

    def rename_logfile(self): # when printing the stdout to log.txt, python tells that now the strings arent ascII but byte strings, so it puts a 'b' before every line, here we get rid of that 'b'
        logfile = os.path.abspath('log.txt')
        a = open(logfile, 'rt')  # opens file in read text mode
        data = a.read()  # reads whole text to variable data
        data = data.replace("b'", "")  # replaces all occurences of manifest-data with newstring
        data = data.replace("'", "")
        a.close()  # closes input file
        a = open(logfile, 'wt')  # opens logfile in write text mode
        a.write(data)  # writes data to logfile
        a.close()  # closes logfile

    def check_log_empty(self): # checks if log.txt is empty, used to keep the popup closed when there is no Analysis running
        logfile = os.path.abspath('log.txt')
        if os.stat(logfile).st_size > 0:
            return True
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('Please run Analysis first')
            self.pop_up.open()

    def check_sixteens_analysis(self, dt):
        try:
            sixteensuserpath
        except NameError:
            pass
        else:
            jobname = os.path.basename(os.path.abspath(sixteensuserpath))
        if self.sixteenschecker is 0:
            self.sixteensstatus = 'Waiting vor Jobs'
        if self.sixteenschecker is 1:
            self.sixteensstatus = 'Job in queue'
        if self.sixteenschecker is 2:
            self.sixteensstatus = '%s \n Job is running' % jobname
        if self.sixteenschecker is 3:
            self.sixteensstatus = '%s \n Job completed' % jobname
        if self.sixteenschecker < 0:
            print('Something is wrong with your code, < 0')


    def set_sixteenschecker_zero(self):  # sets the sixteenschecker back to zero when a new analysis is started
        print(self.sixteenschecker)
        if self.sixteenschecker is 0:
            self.sixteenschecker = self.sixteenschecker
        if self.sixteenschecker is 1:
            self.sixteenschecker = self.sixteenschecker - 1
        if self.sixteenschecker is 2:
            self.sixteenschecker = self.sixteenschecker - 2
        if self.sixteenschecker is 3:
            self.sixteenschecker = self.sixteenschecker - 3
        if self.sixteenschecker is 4:
            self.sixteenschecker = self.sixteenschecker - 4
        if self.sixteenschecker is 5:
            self.sixteenschecker = self.sixteenschecker - 5
        if self.sixteenschecker < 0 or self.sixteenschecker > 2:
            print('Your code is faulty')


    def check_bgc_analysis(self, dt):
        try:
            bgcuserpath
        except NameError:
            pass
        else:
            jobname = os.path.basename(os.path.abspath(bgcuserpath))
        if self.bgcchecker is 0:
            self.bgcstatus = 'Waiting vor Jobs'
        if self.bgcchecker is 1:
            self.bgcstatus = 'Job in queue'
        if self.bgcchecker is 2:
            self.bgcstatus = '%s \n Job is running' % jobname
        if self.bgcchecker is 3:
            self.bgcstatus = '%s \n Job completed' % jobname
        if self.bgcchecker < 0:
            print('Something is wrong with your code, < 0')

    def set_bgcchecker_zero(self):  # sets the sixteenschecker back to zero when a new analysis is started
        if self.bgcchecker is 0:
            self.bgcchecker = self.bgcchecker
        if self.bgcchecker is 1:
            self.bgcchecker = self.bgcchecker - 1
        if self.bgcchecker is 2:
            self.bgcchecker = self.bgcchecker - 2
        if self.bgcchecker is 3:
            self.bgcchecker = self.bgcchecker - 3
        if self.bgcchecker < 0 or self.bgcchecker > 2:
            print('Your code is faulty')


    def check_shotgun_analysis(self, dt):
        try:
            shotgunuserpath
        except NameError:
            pass
        else:
            jobname = os.path.basename(os.path.abspath(shotgunuserpath))
        if self.shotgunchecker is 0:
            self.shotgunstatus = 'Waiting vor Jobs'
        if self.shotgunchecker is 1:
            self.shotgunstatus = 'Job in queue'
        if self.shotgunchecker is 2:
            self.shotgunstatus = '%s \n Job is running' % jobname
        if self.shotgunchecker is 3:
            self.shotgunstatus = '%s \n Job completed' % jobname
        if self.shotgunchecker < 0:
            print('Something is wrong with your code, < 0')


    def set_shotgunchecker_zero(self):  # sets the sixteenschecker back to zero when a new analysis is started
        if self.shotgunchecker is 0:
            self.shotgunchecker = self.shotgunchecker
        if self.shotgunchecker is 1:
            self.shotgunchecker = self.shotgunchecker - 1
        if self.shotgunchecker is 2:
            self.shotgunchecker = self.shotgunchecker - 2
        if self.shotgunchecker is 3:
            self.shotgunchecker = self.shotgunchecker - 3
        if self.shotgunchecker < 0 or self.shotgunchecker > 2:
            print('Your code is faulty')

    def check_jobfolder_sixteens(self): # used in sixteens checks wether a pipelinename exists and a domainname is selected in bgc amplicon, if so calls associated popup
        if os.path.getsize(os.path.abspath('pipelinename.txt')) > 0:
            if self.forbid_sixteens() is False:
                return True
            else:
                Factory.DeselectDomainnamePopup().open()
        else:
            self.newpipe_pop = Factory.NewPipelinenamePopup()
            self.newpipe_pop.update_newpipe_text('Must provide Projectname first')
            self.newpipe_pop.open()

    def check_jobfolder_bgc(self): # used in bgc, checks wether a pipelinename exists and a domainname is selected in bgc amplicon, if so calls associated popup
        if os.path.getsize(os.path.abspath('pipelinename.txt')) > 0:
            if self.forbid_sixteens() is True:
                return True
            else:
                Factory.NoDomainnamePopup().open()
        else:
            self.newpipe_pop = Factory.NewPipelinenamePopup()
            self.newpipe_pop.update_newpipe_text('Must provide Projectname first')
            self.newpipe_pop.open()

    def check_jobfolder_shotguntax(self): # used in shotgun taxonomy, checks wether a pipelinename exists and a domainname is selected in bgc amplicon, if so calls associated popup
        if os.path.getsize(os.path.abspath('pipelinename.txt')) > 0:
            if self.forbid_shotguntaxprofiling() is False:
                return True
            else:
                if self.shotgundomain_domainname() is True: # if user resets shotgun domain name (value) to domainname shotgun tax profiling runs
                    return True
                else:
                    Factory.DeselectDomainnamePopup().open()
        else:
            self.newpipe_pop = Factory.NewPipelinenamePopup()
            self.newpipe_pop.update_newpipe_text('Must provide Projectname first')
            self.newpipe_pop.open()

    def check_jobfolder_shotgundom(self): # used in shotgun taxonomy, checks wether a pipelinename exists and a domainname is selected in bgc amplicon, if so calls associated popup
        if os.path.getsize(os.path.abspath('pipelinename.txt')) > 0:
            if self.forbid_shotguntaxprofiling() is True:
                return True
            else:
                if self.shotgundomain_domainname() is True: # if user resets shotgun domain name (value) to domainname shotgun tax profiling runs
                    return False
                else:
                    Factory.NoDomainnamePopup().open()
        else:
            self.newpipe_pop = Factory.NewPipelinenamePopup()
            self.newpipe_pop.update_newpipe_text('Must provide Projectname first')
            self.newpipe_pop.open()



    def open_config_file(self): # opens config-file for sixteens cofiguration changes
        txt = os.path.abspath('config-file.txt')
        subprocess.run(['open', txt], check=True)

    def get_configuration_sixteens(self): # reads config-file.txt and gets configurations
        txt = os.path.abspath('config-file.txt')

        global no1
        no1 = linecache.getline(txt, 5)
        global no2
        no2 = linecache.getline(txt, 6)
        global no3
        no3 = linecache.getline(txt, 7)
        global no4
        no4 = linecache.getline(txt, 8)
        global no5
        no5 = linecache.getline(txt, 9)
        global no6
        no6 = linecache.getline(txt, 10)

        self.pop_up = Factory.ProbarPopup()
        self.pop_up.update_pop_up_text('Configuration successful')
        self.pop_up.open()

    def check_no1(self): # checks wether no1 is defined, and by that checks wether configurations were made. Called in configurate_sixteens_shell, so that doesnt break if no configs were made
        try:
            no1
        except NameError:
            return False
        else:
            return True


    def configurate_sixteens_shell(self): # configurates shell, called in sixteens_analysis, independent from get_configuration... to make configurations independent from current run!
        if self.check_no1() is True:
            txt = os.path.abspath('config-file.txt')
            shell = os.path.abspath('16Spipeline_qiime2v2019v4docker_gui_v1.sh')
            '''  
            global no1
            no1 = linecache.getline(txt, 5)
            global no2
            no2 = linecache.getline(txt, 6)
            global no3
            no3 = linecache.getline(txt, 7)
            global no4
            no4 = linecache.getline(txt, 8)
            global no5
            no5 = linecache.getline(txt, 9)
            global no6
            no6 = linecache.getline(txt, 10)'''


            a = open(shell, 'rt')
            data = a.read()
            data = data.replace(' --p-trim-left-f 0', no1)
            data = data.replace(' --p-trim-left-r 0', no2)
            data = data.replace(' --p-trunc-len-f 300', no3)
            data = data.replace(' --p-trunc-len-r 300', no4)
            data = data.replace(' --p-sampling-depth 1500', no5)
            data = data.replace(' --p-max-depth 4000', no6)
            a.close()

            a = open(shell, 'wt')
            a.write(data)
            a.close()

            self.delete_configfile() # deletes configuered config file after changing the shell file
            self.replace_configfile() # replaces config-file with new, default one, necessary that early so new analysisis can be queued on default

            '''self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('Configuration successful')
            self.pop_up.open()'''
        else:
            pass # if no configs, dont do anything

    def setback_configfile(self): # after changing shell, config-file gets set back to default
        if self.check_no1() is True:
            txt = txt = os.path.abspath('config-file.txt')

            a = open(txt, 'rt')
            data = a.read()
            data = data.replace(no1, ' --p-trim-left-f 0\n')
            data = data.replace(no2, ' --p-trim-left-r 0\n')
            data = data.replace(no3, ' --p-trunc-len-f 300\n')
            data = data.replace(no4, ' --p-trunc-len-r 300\n')
            data = data.replace(no5, ' --p-sampling-depth 1500\n')
            data = data.replace(no6, ' --p-max-depth 4000\n')
            a.close()

            a = open(txt, 'wt')
            a.write(data)
            a.close()
        else:
            pass


    def replace_sixteensshell(self): # after every run the 'used' shell is replaced by a new, DEFAULT one
        newfile = os.path.abspath('shell_template/16Spipeline_qiime2v2019v4docker_gui_v1.sh')
        workingdir = os.path.abspath('')
        shutil.copy(newfile, workingdir)

    def replace_configfile(self):
        newfile = os.path.abspath('config_template/config-file.txt')
        workingdir = os.path.abspath('')
        shutil.copy(newfile, workingdir)

    def check_manifest_sixteens(self): #checks wether a manifest has been selected by the user (used in whichrun_sixteens to determine wether sixteens_ or result_run
        try:
            sixteensmanifest
        except NameError:
            pass
        else:
            return True

    def check_metadata_sixteens(self):
        try:
            metadata
        except NameError:
            pass
        else:
            return True

    def check_manifest_bgc(self):
        try:
            bgcmanifest
        except NameError:
            pass
        else:
            return True

    def check_manifest_shotgundom(self):
        try:
            bgcmanifest
        except NameError:
            pass
        else:
            return True


    def check_display_sixteens(self):
        if self.sixteensmanifestdisplay != '' and self.sixteensmetadatadisplay != '' and self.sixteensfastqdisplay != '':
            return True
        else:
            return False


    def check_display_bgc(self):
        if self.bgcmanifestdisplay != '' and self.bgcfastqdisplay != '' and self.forbid_sixteens() is True:
            return True
        else:
            return False

    def check_display_shotguntax(self):
        if self.shotguntaxmanifestdisplay != '' and self.shotguntaxfastqdisplay != '':
            return True
        else:
            return False

    def check_display_shotgundom(self):
        if self.shotgundommanifestdisplay != '' and self.shotgundomfastqdisplay != '':
            print('True')
            return True
        else:
            return False


    def check_analysis_sixteens(self): # checks wether a analysis is already running and all parameters were selected
        if self.sixteenschecker == 0 or self.sixteenschecker == 3:
            if self.check_display_sixteens() is True:
                Factory.AnalysisPopup().open()
                return True
            else:
                Factory.ParameterPopup().open()
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text("Can't start new Job \n while other Job is running")
            self.pop_up.open()


    def check_analysis_bgc(self): # checks wether a analysis is already running and all parameters were selected
        if self.bgcchecker == 0 or self.bgcchecker == 3:
            if self.check_display_bgc() is True:
                Factory.AnalysisPopup().open()
                return True
            else:
                Factory.ParameterPopup().open()
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text("Can't start new Job \n while other Job is running")
            self.pop_up.open()


    def check_analysis_shotgun(self): # checks wether a analysis is already running and all parameters were selected
        if self.shotgunchecker == 0 or self.shotgunchecker == 3:
            if self.check_display_shotguntax() is True or self.check_display_shotgundom() is True:
                Factory.AnalysisPopup().open()
                return True
            else:
                Factory.ParameterPopup().open()
        else:
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text("Can't start new Job \n while other Job is running")
            self.pop_up.open()







    def checker(self):  # gets called by bio button on landing, used to test single functions
        self.get_htmlhyperlinks_sixteens()



    # +++++++++++++++++++++++++++++++++++++++++++
    # DISPLAY FUNCTIONS (USED TO DISPLAY FILES, ETC FOR THE USER)
    # +++++++++++++++++++++++++++++++++++++++++++

    def get_pipelinedisplay(self): # gets pipelinedisplay in the app
        self.pipelinename_popup.get_pipelinedisplay()

    def get_projectdisplay(self):
        self.projectname_popup.get_projectdisplay()

    def get_shell(self, filename):  # gives user-selected shell file and displays it in the associated label
        global shell
        shell = '%s' % filename[0]
        if shell.endswith('.sh'):
            self.customshell = os.path.basename(shell)
        else:
            print('Wrong file type chosen')


    def get_sixteensmanifest(self, filename): # gets  selection of manifest-file and stores it in a variable
        global sixteensmanifest
        if len(filename) > 0:
            sixteensmanifest = '%s' % filename[0]
            self.sixteensmanifestchooser = sixteensmanifest

        self.sixteensmanifestdisplay = os.path.basename(os.path.dirname(sixteensmanifest)) + '/' + os.path.basename(sixteensmanifest)


    def get_sixteensmetadata(self, filename):
        global metadata
        if len(filename) > 0: # necessary, because otherwise
            metadata = '%s' % filename[0]
            if metadata.endswith('.tsv'):
                self.metadatachooser = metadata
                self.sixteensmetadatadisplay = os.path.basename(os.path.dirname(metadata)) + '/' + os.path.basename(metadata)
            else:
                print('Wrong file type chosen')

    def get_sixteensfastq(self, filename):
        global fastqfiles
        fastqfiles = filename
        dirname = filename[0]
        dirlength = len(os.path.dirname((dirname))) # necessary to get len of path til fastq files
        fastqbases = []  # list which will contain bases
        for z in fastqfiles:
            fastqbases.append(z[dirlength + 1:]) # only the bases
        self.sixteensfastqdisplay = '\n'.join(map(str, fastqbases))


    def get_bgcmanifest(self, filename): # gets  selection of manifest-file and stores it in a variable
        global bgcmanifest
        if len(filename) > 0:
            bgcmanifest = '%s' % filename[0]
            self.bgcmanifestchooser = bgcmanifest

        self.bgcmanifestdisplay = os.path.basename(os.path.dirname(bgcmanifest)) + '/' + os.path.basename(bgcmanifest)



    def get_bgcfastq(self, filename):
        global bgcfastqfiles
        bgcfastqfiles = filename
        dirname = filename[0]
        dirlength = len(os.path.dirname((dirname))) # necessary to get len of path til fastq files
        fastqbases = []  # list which will contain bases
        for z in bgcfastqfiles:
            fastqbases.append(z[dirlength + 1:]) # only the bases
        self.bgcfastqdisplay = '\n'.join(map(str, fastqbases))


    def get_shotguntaxmanifest(self, filename): # gets  selection of manifest-file and stores it in a variable
        global shotguntaxmanifest
        if len(filename) > 0:
            shotguntaxmanifest = '%s' % filename[0]

        self.shotguntaxmanifestdisplay = os.path.basename(os.path.dirname(shotguntaxmanifest)) + '/' + os.path.basename(shotguntaxmanifest)

    def get_shotguntaxfastq(self, filename):
        global shotguntaxfastqfiles
        shotguntaxfastqfiles = filename
        dirname = filename[0]
        dirlength = len(os.path.dirname((dirname))) # necessary to get len of path til fastq files
        fastqbases = []  # list which will contain bases
        for z in shotguntaxfastqfiles:
            fastqbases.append(z[dirlength + 1:]) # only the bases
        self.shotguntaxfastqdisplay = '\n'.join(map(str, fastqbases))

    def get_shotgundommanifest(self, filename): # gets  selection of manifest-file and stores it in a variable
        global shotgundommanifest
        if len(filename) > 0:
            shotgundommanifest = '%s' % filename[0]

        self.shotgundommanifestdisplay = os.path.basename(os.path.dirname(shotgundommanifest)) + '/' + os.path.basename(shotgundommanifest)

    def get_shotgundomfastq(self, filename):
        global shotgundomfastqfiles
        shotgundomfastqfiles = filename
        dirname = filename[0]
        dirlength = len(os.path.dirname((dirname))) # necessary to get len of path til fastq files
        fastqbases = []  # list which will contain bases
        for z in shotgundomfastqfiles:
            fastqbases.append(z[dirlength + 1:]) # only the bases
        self.shotgundomfastqdisplay = '\n'.join(map(str, fastqbases))















    '''def get_sixteensdisplay(self):  # gives user-selected manifest-data and the according fastq files and displays it in the associated label
        self.sixteensmanifestdisplay = os.path.basename(os.path.dirname(manifest)) + '/' +  os.path.basename(manifest)

        self.sixteensmetadatadisplay = os.path.basename(os.path.dirname(metadata)) + '/' +  os.path.basename(metadata)

        chosenpath = os.path.dirname(manifest)
        fastqfiles = [(f.split('.'))[0] for f in os.listdir(chosenpath) if f.endswith('.gz')]
        print('\n'.join(map(str, fastqfiles)))
        self.sixteensfastqdisplay = '\n'.join(map(str, fastqfiles))'''










    # +++++++++++++++++++++++++++++++++++++++++++
    # 16s RESULT FUNCTIONS
    # +++++++++++++++++++++++++++++++++++++++++++

    def move_preview_files_sixteens(self, symlinks=False, ignore=None): # moves certain (important) result files to the workingdir to display them in a preview html file
        all_files = [] # list in which all files that should be viewed in preview get stored
        all_folders = []
        newroot = os.path.abspath('%s' % sixteensresultpath)
        previewdir = os.path.abspath('Preview')
        dest = '%s/data' % previewdir # creates new dir in chosen path with same name as the projectfolder
        files = glob.glob('%s/**/*index.html' % sixteensresultpath, recursive=True)

        all_files.extend(files)
        for files in all_files:
            shutil.copy(files, previewdir)

        '''dist_folder = glob.glob('%s/**/*dist' % sixteensresultpath, recursive=True)
        q2templateassets_folder = glob.glob('%s/**/*q2templateassets' % sixteensresultpath, recursive=True)
        css_folder = glob.glob('%s/**/*css' % sixteensresultpath, recursive=True)
        img_folder = glob.glob('%s/**/*img' % sixteensresultpath, recursive=True)
        js_folder = glob.glob('%s/**/*js' % sixteensresultpath, recursive=True)
        templates_folder = glob.glob('%s/**/*templates' % sixteensresultpath, recursive=True)
        vendor_folder = glob.glob('%s/**/*vendor' % sixteensresultpath, recursive=True)

        for root, dirs, files in os.walk(newroot):
            dist_folder
            q2templateassets_folder
            css_folder
            img_folder
            js_folder
            templates_folder
            vendor_folder
        all_folders.extend(dist_folder + q2templateassets_folder + img_folder + templates_folder + vendor_folder + css_folder + js_folder)'''





    def get_csv_sixteenspreview(self): # creates html tables from created result files, moves html file to project dir, moves new, 'unused' sixteenspreview.html to preview dir
        '''sixteens_table1 = os.path.abspath('{0}/{1}/{2}/per-sample-fastq-counts.csv'.format(pipelinefolder, userfolder, sixteens_name))
        sixteens_table2 = os.path.abspath('{0}/{1}/{2}/metadata.csv'.format(pipelinefolder, userfolder, sixteens_name))
        sixteens_table3 = os.path.abspath('{0}/{1}/{2}/descriptive_stats.tsv'.format(pipelinefolder, userfolder, sixteens_name))'''

        sixteens_html = os.path.abspath('Preview/sixteenspreview.html')

        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/per-sample-fastq-counts.csv' % sixteensresultpath, recursive=True))):
            csv1 = pd.read_csv('%s' % "','".join(glob.glob('%s/*/**/per-sample-fastq-counts.csv' % sixteensresultpath, recursive=True)))
        else: pass
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/metadata.csv' % sixteensresultpath, recursive=True))):
            csv2 = pd.read_csv('%s' % "','".join(glob.glob('%s/*/**/metadata.csv' % sixteensresultpath, recursive=True)), sep='\t')
        else: pass
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/descriptive_stats.tsv' % sixteensresultpath, recursive=True))):
            csv3 = pd.read_csv('%s' % "','".join(glob.glob('%s/*/**/descriptive_stats.tsv' % sixteensresultpath, recursive=True)), sep='\t')
        else: pass
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/sample-frequency-detail.csv' % sixteensresultpath, recursive=True))):
            csv4 = pd.read_csv('%s' % "','".join(glob.glob('%s/*/**/sample-frequency-detail.csv' % sixteensresultpath, recursive=True)), sep='\t')
        else: pass
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/evenness-group-significance_metadata.tsv' % sixteensresultpath, recursive=True))):
            csv5 = pd.read_csv('%s' % "','".join(glob.glob('%s/*/**/evenness-group-significance_metadata.tsv' % sixteensresultpath, recursive=True)), sep='\t')
        else: pass
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/faith-pd-group-significance_metadata.tsv' % sixteensresultpath, recursive=True))):
            csv6 = pd.read_csv('%s' % "','".join(glob.glob('%s/*/**/faith-pd-group-significance_metadata.tsv' % sixteensresultpath, recursive=True)), sep='\t')
        else: pass


        try: csv1
        except NameError: sixteenshtml_table1 = 'cant find per-sample-fastq-counts.csv'
        else:
            sixteenshtml_table1 = csv1.to_html()
        try: csv2
        except NameError: sixteenshtml_table2 = 'cant find metadata.tsv'
        else:
            sixteenshtml_table2 = csv2.to_html()
        try: csv3
        except NameError: sixteenshtml_table3 = 'cant find descriptive_stats.tsv.tsv'
        else:
            sixteenshtml_table3 = csv3.to_html()
        try: csv4
        except NameError: sixteenshtml_table4 = 'cant find sample-frequency-detail.tsv'
        else:
            sixteenshtml_table4 = csv4.to_html()
        try: csv5
        except NameError:
            sixteenshtml_table5 = 'cant find evenness-group-signficance_metadata.tsv'
        else:
            sixteenshtml_table5 = csv5.to_html()
        try:csv6
        except NameError:
            sixteenshtml_table6 = 'cant find faith-pd-group-significance_metadata.tsv'
        else:
            sixteenshtml_table6 = csv6.to_html()




        a = open(sixteens_html, 'rt')
        data = a.read()
        data = data.replace('cant find per-sample-fastq-counts.csv', sixteenshtml_table1)
        data = data.replace('cant find metadata.tsv', sixteenshtml_table2)
        data = data.replace('cant find descriptive_stats.tsv', sixteenshtml_table3)
        data = data.replace('cant find sample-frequency-detail.tsv', sixteenshtml_table4)
        data = data.replace('evenness-group-signficance_metadata.tsv', sixteenshtml_table5)
        data = data.replace('cant find faith-pd-group-significance_metadata.tsv', sixteenshtml_table6)
        a.close()

        a = open(sixteens_html, 'wt')
        a.write(data)
        a.close()

        projectdir = os.path.abspath('{0}/{1}'.format(pipelinefolder, userfolder))
        shutil.move(sixteens_html, projectdir)

        self.replace_sixteenspreview()


    def get_htmlhyperlinks_sixteens(self):
        sixteens_html = os.path.abspath('Preview/sixteenspreview.html')
        htmllist = []
        htmlbases = []
        linkstringpre = '<br> <a href = "'
        linkstringpost = '" target="_blank" > %s </a>' # gives a variable that can be filled when replacing strings later

        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/paired-end-demux_index.html' % sixteensresultpath, recursive=True))):
            pairedindex = '%s' % "','".join(glob.glob('%s/*/**/paired-end-demux_index.html' % sixteensresultpath, recursive=True))
        else: pairedindex = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/denoising-stats_index.html' % sixteensresultpath, recursive=True))):
            denoisingindex = '%s' % "','".join(glob.glob('%s/*/**/denoising-stats_index.html' % sixteensresultpath, recursive=True))
        else: denoisingindex = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/table_index.html' % sixteensresultpath, recursive=True))):
            tableindex = '%s' % "','".join(glob.glob('%s/*/**/table_index.html' % sixteensresultpath, recursive=True))
        else: tableindex = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/rep-seqs_index.html' % sixteensresultpath, recursive=True))):
            repindex = '%s' % "','".join(glob.glob('%s/*/**/rep-seqs_index.html' % sixteensresultpath, recursive=True))
        else: repindex = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/weighted_unifrac_emperor_index.html' % sixteensresultpath, recursive=True))):
            wi = '%s' % "','".join(glob.glob('%s/*/**/weighted_unifrac_emperor_index.html' % sixteensresultpath, recursive=True))
        else: wi = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/bray_curtis_emperor_index.html' % sixteensresultpath, recursive=True))):
            bci = '%s' % "','".join(glob.glob('%s/*/**/bray_curtis_emperor_index.html' % sixteensresultpath, recursive=True))
        else:   bci = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/unweighted_unifrac_emperor_index.html' % sixteensresultpath, recursive=True))):
            uuei= '%s' % "','".join(glob.glob('%s/*/**/unweighted_unifrac_emperor_index.html' % sixteensresultpath, recursive=True))
        else: uuei= ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/jaccard_emperor_index.html' % sixteensresultpath, recursive=True))):
            jei = '%s' % "','".join(glob.glob('%s/*/**/jaccard_emperor_index.html' % sixteensresultpath, recursive=True))
        else: jei = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/evenness-group-significance_index.html' % sixteensresultpath, recursive=True))):
            egsi = '%s' % "','".join(glob.glob('%s/*/**/evenness-group-significance_index.html' % sixteensresultpath, recursive=True))
        else: egsi = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/faith-pd-group-significance_index.html' % sixteensresultpath, recursive=True))):
            fpdgsi = '%s' % "','".join(glob.glob('%s/*/**/faith-pd-group-significance_index.html' % sixteensresultpath, recursive=True))
        else: fpdgsi = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/unweighted_unifrac_layer_significance_index.html' % sixteensresultpath, recursive=True))):
            uulsi = '%s' % "','".join(glob.glob('%s/*/**/unweighted_unifrac_layer_significance_index.html' % sixteensresultpath, recursive=True))
        else: uulsi = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/unweighted_unifrac_site_significance_index.html' % sixteensresultpath, recursive=True))):
            uussi = '%s' % "','".join(glob.glob('%s/*/**/unweighted_unifrac_site_significance_index.html' % sixteensresultpath, recursive=True))
        else: uussi = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/taxonomy_index.html' % sixteensresultpath, recursive=True))):
            ti = '%s' % "','".join(glob.glob('%s/*/**/taxonomy_index.html' % sixteensresultpath, recursive=True))
        else: ti = ''
        if os.path.exists('%s' % "','".join(glob.glob('%s/*/**/taxa-bar-plots_index.html' % sixteensresultpath, recursive=True))):
            tbpi= '%s' % "','".join(glob.glob('%s/*/**/taxa-bar-plots_index.html' % sixteensresultpath, recursive=True))
        else: tbpi = ''
        pathlen = len(os.path.dirname(os.path.dirname(pairedindex)))

        htmllist.extend((pairedindex, denoisingindex, tableindex, repindex, wi, bci, uuei, jei, egsi, fpdgsi, uulsi, uussi, ti, tbpi))
        print(htmllist)

        htmlbases = [z[pathlen + 1:] for z in htmllist]

        linklist = [linkstringpre + s + linkstringpost for s in htmlbases]

        a = open(sixteens_html, 'rt')
        data = a.read()
        data = data.replace('<p> Cant find paired-end-demux index.html </p>', linklist[0] % 'paired-end-demux_index.html')
        data = data.replace('<p> Cant find denoising-stats index.html </p>', linklist[1] % 'denoising-stats_index.html')
        data = data.replace('<p> Cant find table index.html </p>', linklist[2] % 'table_index.html')
        data = data.replace('<p> Cant find rep-seqs index.html </p>', linklist[3] % 'rep-seqs_index.html')
        data = data.replace('<p> Cant find weighted_unifrac_emperor index.html </p>', linklist[4] % 'weighted_unifrac_emperor_index.html')
        data = data.replace('<p> Cant find bray_curtis_emperor index.htm l</p>', linklist[5] % 'bray_curtis_emperor_index.html')
        data = data.replace('<p> Cant find unweighted_unifrac_emperor index.html </p>', linklist[6] %  'unweighted_unifrac_emperor_index.html')
        data = data.replace('<p> Cant find jaccard_emperor index.html </p>', linklist[7] % 'jaccard_emperor_index.html')
        data = data.replace('<p> Cant find evenness-group-significance index.html </p>', linklist[8] % 'evenness-group-significance_index.html')
        data = data.replace('<p> Cant find faith-pd-group-significance index.html </p>', linklist[9] % 'faith-pd-group-significance_index.html')
        data = data.replace('<p> Cant find unweighted_unifrac_layer_significance index.html </p>', linklist[10] % 'unweighted_unifrac_layer_significance_index.html')
        data = data.replace('<p> Cant find unweighted_unifrac_site_significance index.html </p>', linklist[11] % 'unweighted_unifrac_site_significance_index.html')
        data = data.replace('<p> Cant find taxonomy index.html</p>', linklist[12] % 'taxonomy_index.html')
        data = data.replace('<p> Cant find taxa-bar-plots index.html</p>', linklist[13] % 'taxa-bar-plots_index.html')

        a = open(sixteens_html, 'wt')
        a.write(data)
        a.close()




    def replace_sixteenspreview(self): # replaces filled sixteenspreview.html with empty one after closing the gui
        newfile = os.path.abspath('html_template/sixteenspreview.html')
        previewdir = os.path.abspath('Preview')
        shutil.copy(newfile, previewdir)


    # -------------------------
    # PNG Views
    # -------------------------

    def pngpopup_demultiplex_summary(self):  # opens the png file generated by run_sixteens in a popup from paired-end-demux
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/demultiplex-summary.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                            pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()

    def pnglabel_demultiplex_summary_preview(self):
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/demultiplex-summary.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            self.previewsource = png_string
        else:
            self.check_result()

    def pngpopup_sample_frequencies(self):  # table.qzv
        if self.check_sixteens() is True:
            png_file = glob.glob('%%s/*/**/sample-frequencies.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()


    def pngpopup_feature_frequencies(self):  # table.qzv
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/feature-frequencies.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()

    def pngpopup_cambisolboxplots(self):  # unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/Cambisol-boxplots.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()


    def pngpopup_podsolboxplots(self):  # unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/Podsol-boxplots.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()


    def pngpopup_gleyboxplots(self): # unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/Gley-boxplots.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()

    def pngpopup_aboxplots(self): # unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/A-boxplots.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()

    def pngpopup_bboxplots(self): # unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/B-boxplots.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()

    def pngpopup_oboxplots(self): # unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            png_file = glob.glob('%s/*/**/O-boxplots.png' % sixteensresultpath, recursive=True)
            png_string = '%s' % "','".join(png_file)
            if os.path.isfile(png_string):
                content = Image(source=png_string,
                                size_hint=(.9, .9),
                                allow_stretch=True)
                pngpop = Popup(title='png', content=content, size_hint=(None, None), size=(1500, 1200),
                               pos_hint=({'center_x': .5, 'center_y': .5}))
                pngpop.open()
            else:
                self.check_result()




    # -------------------------
    # CSV Views
    # -------------------------



    def open_csv_reverseseven(self):  # opens csv file in excel from paired-end-demux
        if self.check_sixteens() is True:  # calls check_sixteens to determine if sixteens_name exists, if yes, runs the function
            csv_file = glob.glob('%s/*/**/reverse-seven-number-summaries.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ','\ ')  # if there is a space in the path(e.g. /mebigeasy test/GUI...), thism makes it executable for the System, because it changes it to (/mebigeasy\ test) and that is readable for the system
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_fowardseven(self):  # paired-end-demux
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/forward-seven-number-summaries.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ','\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_persamplefastq(self):  # paired-end-demux
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/per-sample-fastq-counts.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ','\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_samplefreqdetail(self): # table.qzv
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/sample-frequency-detail.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_featurefreqdetail(self): # table.qzv
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/feature-frequency-detail.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_faithpd(self): # alpha-rarefaction
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/faith_pd.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_observedotus(self): # alpha-rarefaction
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/observed_otus.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_shannon(self): # alpha-rarefaction
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/shannon.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_1(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-1.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_2(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-2.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_3(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-3.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_4(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-4.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_5(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-5.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_6(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-6.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_7(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-7.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_8(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-8.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_9(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-9.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_10(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-10.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_11(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-11.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_12(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-12.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_13(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-13.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_14(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-14.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_taxabarlevels_15(self):
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/level-15.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_evennesskruskallayer(self): #evenness-group-significance
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/evenness-group-significance_kruskal-wallis-pairwise-Layer.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_evennesskruskalsite(self): #evenness-group-significance
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/evenness-group-significance_kruskal-wallis-pairwise-Site.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_faithpdskruskallayer(self): # faith-pd-group-significance
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/faith-pd-group-significance_kruskal-wallis-pairwise-Layer.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_faithpdkruskalsite(self): # faith-pd-group-significance
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/faith-pd-group-significance_kruskal-wallis-pairwise-Site.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_unweightedsitepermanova(self): # unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/unweighted-unifrac-site-significance_permanova-pairwise.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_unweightedlayerpermanova(self): # unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            csv_file = glob.glob('%s/*/**/unweighted-unifrac-layer-significance_permanova-pairwise.csv' % sixteensresultpath, recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ', '\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    # -------------------------
    # TSV Views
    # -------------------------

    def open_tsv_seven_number(self): # rep-seqs
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/seven_number_summary.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_descriptive_stats(self): # rep-seqs
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/descriptive_stats.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()


    def open_tsv_taxa_metadata(self): # taxa-barplot
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/taxa-bar-plots_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_braycurtis_metadata(self): # bray-curtis-emperor
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/bray_curtis_emperor_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_evenness_metadata(self): # evenness group sig
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/evenness-group-significance_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_faith_metadata(self): # faith pd
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/faith-pd-group-significance_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_jaccard_metadata(self): # jaccard-emperor
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/jaccard_emperor_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_unifraclayer_metadata(self): # unweighted unifrac layer significance
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/unweighted-unifrac-layer-significance_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_unifracsite_metadata(self):  # unweighted unifrac layer significance
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/unweighted-unifrac-site-significance_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_unifracemperor_metadata(self):  # unweighted unifrac emperor
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/unweighted_unifrac_emperor_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_weightedunifracemperor_metadata(self):  # weighted unifrac emperor
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/weighted_unifrac_emperor_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_denloising_metadata(self):  # denoising-stats
        if self.check_sixteens() is True:
            tsv_file = glob.glob('%s/*/**/denoising-stats_metadata.tsv' % sixteensresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()




    # -------------------------
    # HTML Views
    # -------------------------

    def open_html_preview_sixteens(self):  # opens a new tab containing the html file from paired-end-demux
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/sixteenspreview.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Preview', html_string, width=1200, height=800)
                webview.start()

    def open_html_browser_plot(self):  # opens a new tab containing the html file from paired-end-demux
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/quality-plot.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                #filename = 'file:///%s' % html_string
                #webbrowser.open(filename, new=1)
                webview.create_window('Quality Plot', html_string)
                webview.start()
            else:
                self.check_result()




    def open_html_overview_preview(self):
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/overview.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                #os.system('webkit2png quality-plot.html -o  quality-plot.png')
                os.system('webkit2png %s -o  quality-plot.png' % html_string)
                html_source = os.path.abspath('quality-plot.png-full.png')
            self.previewsource = html_source
        else:
            self.check_result()


    def open_html_browser_overview(self):
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/overview.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Overview', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_overview_preview(self):
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/overview.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                #os.system('webkit2png quality-plot.html -o  quality-plot.png')
                os.system('webkit2png %s -o  quality-plot.png' % html_string)
                html_source = os.path.abspath('quality-plot.png-full.png')
            self.previewsource = html_source
        else:
            self.check_result()

    def open_html_pairedendindex(self):  # rep-seqs
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/paired-end-demux_index.html' % sixteensresultpath, recursive=True)
            print(html_file)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()



    def open_html_repseqsindex(self):  # rep-seqs
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/rep-seqs_index.html' % sixteensresultpath, recursive=True)
            print(html_file)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_tableindex(self): #table
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/table_index.html' % sixteensresultpath, recursive=True)
            print(html_file)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_featurefreqdetail(self):  # table
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/feature-frequency-detail.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Feature Frequency Detail', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_samplefreqdetail(self):  # table
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/sample-frequency-detail.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Sample Frequency Detail', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_alphaindex(self): # alpha-rarefaction
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/alpha-rarefaction_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_taxabarindex(self): # taxa-bar-plots
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/taxa-bar-plots_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_taxonomyindex(self): # taxonomy
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/taxonomy_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_braycurtisemperor(self):  # bray_curtis_emperor
        if self.check_sixteens() is True:
            if os.path.isfile(os.path.abspath('{0}/{1}/emperor.html'.format(sixteensuserpath, sixteens_name))):
                html_file = os.path.abspath('{0}/{1}/emperor.html'.format(sixteensuserpath, sixteens_name))
                webview.create_window('Emperor', html_file)
                webview.start()
            else:
                self.check_result()

    def open_html_braycurtisindex(self):  # bray_curtis_emperor
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/bray_curtis_emperor_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_evennessgroupindex(self): # evenness_group_significance
            if self.check_sixteens() is True:
                html_file = glob.glob('%s/*/**/evenness_group_significance_index.html' % sixteensresultpath, recursive=True)
                html_string = '%s' % "','".join(html_file)
                if os.path.isfile(html_string):
                    webview.create_window('Index', html_string)
                    webview.start()
                else:
                    self.check_result()

    def open_html_faithpdindex(self): # faith-pd-group-significance
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/faith-pd-group-significance_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_jaccardindex(self): # jaccard_emperor
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/jaccard_emperor_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()


    def open_html_unweightedindex(self): # unweighted_unifrac_emperor
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/unweighted_unifrac_emperor_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_unweightedsiteindex(self): #unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/unweighted-unifrac-site-significance_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_unweightedlayerindex(self): #unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/unweighted-unifrac-layer-significance_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_weightedindex(self):  # weighted_unifrac_emperor
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**/weighted_unifrac_emperor_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()

    def open_html_denoisingindex(self):  # denoising-stats
        if self.check_sixteens() is True:
            html_file = glob.glob('%s/*/**denoising-stats_index.html' % sixteensresultpath, recursive=True)
            html_string = '%s' % "','".join(html_file)
            if os.path.isfile(html_string):
                webview.create_window('Index', html_string)
                webview.start()
            else:
                self.check_result()


    # -------------------------
    # PDF Views
    # -------------------------

    def show_demultiplex_pdf(self):  # opens pdf file demultiplex-summary
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/demultiplex-summary.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_samplefreq_pdf(self):  # table.qzv
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/sample-frequencies.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_featurefreq_pdf(self):  # table.qzv
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/feature-frequencies.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_cambisolboxplot_pdf(self): # unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/Cambisol-boxplots.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_podsolboxplot_pdf(self): # unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/Podsol-boxplots.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_gleyboxplot_pdf(self): # unweighted-unifrac-site-significance
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/Gley-boxplots.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_aboxplot_pdf(self): # unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/A-boxplots.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_bboxplot_pdf(self): # unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/B-boxplots.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_oboxplot_pdf(self): # unweighted-unifrac-layer-significance
        if self.check_sixteens() is True:
            pdf_file = glob.glob('%s/*/**/O-boxplots.pdf' % sixteensresultpath, recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    # +++++++++++++++++++++++++++++++++++++++++++
    # BGC AND SHOTGUN DOMAIN RESULT FUNCTIONS
    # +++++++++++++++++++++++++++++++++++++++++++

    # -------------------------
    # AMP-PDF Functions
    # -------------------------
    def show_out_placementstree_pdf(self):  # opens pdf file demultiplex-summary
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                pdf_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_placements_tree.pdf'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                pdf_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_placements_tree.pdf'.format(bgcresultpath, domainname), recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_nr1_placementstree_pdf(self):  # opens pdf file demultiplex-summary
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                pdf_file = glob.glob('{0}/*/**/{1}_{2}_placements_tree.pdf'.format(shotgunresultpath, namer1, shotgundomain), recursive=True)
            else:
                pdf_file = glob.glob('{0}/*/**/{1}_{2}_placements_tree.pdf'.format(bgcresultpath, namer1, domainname), recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_nr2_placementstree_pdf(self):  # opens pdf file demultiplex-summary
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                pdf_file = glob.glob('{0}/*/**/{1}_{2}_placements_tree.pdf'.format(shotgunresultpath, namer2, shotgundomain), recursive=True)
            else:
                pdf_file = glob.glob('{0}/*/**/{1}_{2}_placements_tree.pdf'.format(bgcresultpath, namer2, domainname), recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_raredivest_pdf(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                pdf_file = glob.glob('{0}/*/**/{1}_rare_div_est.pdf'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                pdf_file = glob.glob('{0}/*/**/{1}_rare_div_est.pdf'.format(bgcresultpath, domainname), recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_bindingmodel_pdf(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                pdf_file = glob.glob('{0}/*/**/{1}_model_div_est.pdf'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                pdf_file = glob.glob('{0}/*/**/{1}_model_div_est.pdf'.format(bgcresultpath, domainname), recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_nr1_violin_pdf(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                pdf_file = glob.glob('{0}/*/**/{1}_{2}_violin_div_est.pdf'.format(shotgunresultpath, namer1, shotgundomain),recursive=True)
            else:
                pdf_file = glob.glob('{0}/*/**/{1}_PKS_KS_violin_div_est.pdf'.format(bgcresultpath, namer1, domainname),recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    def show_nr2_violin_pdf(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                pdf_file = glob.glob('{0}/*/**/{1}_{2}_violin_div_est.pdf'.format(shotgunresultpath, namer2, shotgundomain), recursive=True)
            else:
                pdf_file = glob.glob('{0}/*/**/{1}_{2}_violin_div_est.pdf'.format(bgcresultpath, namer2, domainname), recursive=True)
            pdf_string = '%s' % "','".join(pdf_file)
            if os.path.isfile(pdf_string):
                a = pdf_string.replace(' ', '\ ')
                subprocess.run(['open', a], check=True)
            else:
                self.check_result()

    # -------------------------
    # AMP-TSV Functions
    # -------------------------

    def open_tsv_nr1_bindingmodel(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_model_div_est.tsv'.format(shotgunresultpath, namer1, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_model_div_est.tsv'.format(bgcresultpath, namer1, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_nr1_bindingcluster(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_cluster2abund.tsv'.format(shotgunresultpath, namer1, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_cluster2abund.tsv'.format(bgcresultpath, namer1, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_nr1_bindingsummary(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_summary_model_div_est.tsv'.format(shotgunresultpath, namer1, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_summary_model_div_est.tsv'.format(bgcresultpath, namer1, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ', '\ ')
                # os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_nr2_bindingmodel(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/*/**/{1}_{2}_model_div_est.tsv'.format(shotgunresultpath, namer2, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_model_div_est.tsv'.format(bgcresultpath, namer2, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_nr2_bindingcluster(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/*/**/{1}_{2}_cluster2abund.tsv'.format(shotgunresultpath, namer2, shotgundomain),recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_cluster2abund.tsv'.format(bgcresultpath, namer2, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_nr2_bindingsummary(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_summary_model_div_est.tsv'.format(shotgunresultpath, namer2, shotgundomain),recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_{2}_summary_model_div_est.tsv'.format(bgcresultpath, namer2, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_out_bindingmodel(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_model_div_est.tsv'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_model_div_est.tsv'.format(bgcresultpath, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_out_bindingcluster(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_cluster2abund.tsv'.format(shotgunresultpath, shotgundomain),recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_cluster2abund.tsv'.format(bgcresultpath, domainname),recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_out_bindingsummary(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_summary_model_div_est.tsv'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_summary_model_div_est.tsv'.format(bgcresultpath, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_out_rarediv(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/{1}_rare_div_est.tsv'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_rare_div_est.tsv'.format(bgcresultpath, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_out_raredivsummary(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('{0}/*/**/{1}_summary_rare_div_est.tsv'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                tsv_file = glob.glob('{0}/*/**/{1}_summary_rare_div_est.tsv'.format(bgcresultpath, domainname), recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()

    def open_tsv_out_abundclean(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                tsv_file = glob.glob('%s/*/**/abund2clust_clean.tsv' % shotgunresultpath, recursive=True)
            else:
                tsv_file = glob.glob('%s/*/**/abund2clust_clean.tsv' % bgcresultpath, recursive=True)
            tsv_string = '%s' % "','".join(tsv_file)
            if os.path.isfile(tsv_string):
                a = tsv_string.replace(' ','\ ')
                #os.system('open /Applications/Microsoft\ Excel.app %s' % a)
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, a])
            else:
                self.check_result()


    # -------------------------
    # AMP-CSV Functions
    # -------------------------

    def open_csv_nr1_bindingquery(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                csv_file = glob.glob('{0}/*/**/{1}_{2}_query_info.csv'.format(shotgunresultpath, namer1, shotgundomain), recursive=True)
            else:
                csv_file = glob.glob('{0}/*/**/{1}_{2}_query_info.csv'.format(bgcresultpath, namer1, domainname), recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ','\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_nr2_bindingquery(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                csv_file = glob.glob('{0}/*/**/{1}_{2}_query_info.csv'.format(shotgunresultpath, namer2, shotgundomain), recursive=True)
            else:
                csv_file = glob.glob('{0}/*/**/{1}_{2}_query_info.csv'.format(bgcresultpath, namer2, domainname), recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ','\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()

    def open_csv_out_bindingquery(self):
        if self.check_sixteens() is True:
            if self.check_shotgundomain() is True:
                csv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_query_info.csv'.format(shotgunresultpath, shotgundomain), recursive=True)
            else:
                csv_file = glob.glob('{0}/*/**/out_dom_merged_div_{1}_{1}_query_info.csv'.format(bgcresultpath, domainname),recursive=True)
            csv_string = '%s' % "','".join(csv_file)
            if os.path.isfile(csv_string):
                a = csv_string.replace(' ','\ ')
                os.system('open /Applications/Microsoft\ Excel.app %s' % a)
            else:
                self.check_result()



    # -------------------------
    # Save Functions
    # -------------------------

    def move_pdf(self, path):
        if self.check_sixteens() is True:
            dir = os.path.abspath('{0}/{1}'.format(userfolder, sixteens_name))
            pdf_files = glob.glob('{0}/{1}/*.pdf'.format(userfolder, sixteens_name), recursive=True)
            dest = '%s' % path
            for files in os.walk(dir):
                pdf_files
            for files in pdf_files:
                shutil.copy(files, dest)
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('.pdf-File saved in %s' % dest)
            self.pop_up.open()

    def move_png(self, path):
        if self.check_sixteens() is True:
            dir = os.path.abspath('{0}/{1}'.format(userfolder, sixteens_name))
            png_files = glob.glob('{0}/{1}/*.png'.format(userfolder, sixteens_name), recursive=True)
            dest = '%s' % path
            for files in os.walk(dir):
                png_files
            for files in png_files:
                shutil.copy(files, dest)
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('.png-File saved in %s' % dest)
            self.pop_up.open()


    def move_qzv(self, path):  # s. move_png
        if self.check_sixteens() is True:
            dir = os.path.abspath('{0}/{1}'.format(userfolder, sixteens_name))
            qzv_files = glob.glob('{0}/{1}/*.qzv'.format(userfolder, sixteens_name), recursive=True)
            dest = '%s' % path
            for files in os.walk(dir):
                qzv_files
            for files in qzv_files:
                shutil.copy(files, dest)
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('.qzv-File saved in %s' % dest)
            self.pop_up.open()

    def move_all(self, path):  # if user wants he can save all the results at once (maybe put it all in a folder)
        if self.check_sixteens() is True:
            self.move_pdf(path)
            self.move_png(path)
            self.move_results(path)

    def move_project(self, path): # saves the projectfolder in user chosen directory
        foldername = os.path.basename(pipelinepath)
        if self.check_sixteens() is True:
            projectfolder = pipelinepath
            dest = '{0}/{1}'.format(path, foldername) # creates new dir in chosen path with same name as the projectfolder
            shutil.copytree(projectfolder, dest)
            #dir_util.copy_tree(projectfolder, dest)
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('Projectfolder saved in %s' % dest)
            self.pop_up.open()

    def move_project_shotgun(self, path): # saves the projectfolder in user chosen directory
        foldername = os.path.basename(pipelinepath)
        if self.check_project() is True:
            projectfolder = pipelinepath
            dest = '{0}/{1}'.format(path, foldername) # creates new dir in chosen path with same name as the projectfolder
            shutil.copytree(projectfolder, dest)
            #dir_util.copy_tree(projectfolder, dest)
            self.pop_up = Factory.ProbarPopup()
            self.pop_up.update_pop_up_text('Projectfolder saved in %s' % dest)
            self.pop_up.open()

    def choose_download(self, filename):  # calls move_ functions depending on which filetype is chosen
        file = '%s' % filename
        if file.endswith('.png'):
            self.move_png()
        if file.endswith('.pdf'):
            self.move_pdf()
        if file.endswith('.qzv'):
            self.move_results()



'''
    def selected(self, filename): #prints the in the importchooser selected file (just to check)
        print("selected: %s" % filename[0])
'''



if __name__ == "__main__":
    MeBigEasy().run()
    MeBigEasy().move_projects_to_dir()
    MeBigEasy().delete_files()
    MeBigEasy().delete_manifest_sixteens()
    MeBigEasy().delete_manifest_bgc()
    MeBigEasy().empty_logtext()
    MeBigEasy().empty_pipelinename()
    MeBigEasy().empty_jobname()
    MeBigEasy().delete_sixteensshell() # if user closes app before analysis is finished, 16s shell put back to default
    MeBigEasy().replace_sixteensshell()
    MeBigEasy().delete_configfile() # if user closes app before analysis is finished, config-file put back to default
    MeBigEasy().replace_configfile()
