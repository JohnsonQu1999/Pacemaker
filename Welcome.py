#===ABSTRACTION LAYER===#
# Required inputs: 
# Behaviour:
#  - Draws main GUI with all parameters present - capable of utilizing and managing windows for display of text and graphics
#  - Creates interface for pacing modes
#  - Displays all programmable parameters for review and modification
#  - Capable of processing user positioning and input buttons
#  - Allows user to tell instance what mode they want to edit
#  - Allows user to tell instance what they want the parameters to be
#  - Allows user to tell instance they want to reset parameters to nominal values
#  - Visually indicates when the DCM and device are communicating
#  - Visually indicates when a different pacemaker device is approached than was previously interrogated

#===COMPLETED TODO ITEMS==#
# IDEA: for the edit_XXXX's, instead of making a dedicated method for each mode,
  # Make one that takes care of all of them, and input a string of 1's and 0's which marks which entries
  # we care about, as is page 28 of the PACEMAKER document
  # Issues: how do we determine mode? maybe check against a dictionary
  # PREREQ's: 1.) modify data storage string format (needs to include all 25 options for each mode,
  # with NA's anywhere it's not applicable)										COMPLETED
  # 2.) edit __check_In_Range - PSEUDO CODE WRITTEN								COMPLETED
  # 3.) edit __get_Vals - PSEUDO CODE WRITTEN									COMPLETED
  # 4.) replace edit_XXX's with 1 function - PSEUDO CODE WRITTEN				COMPLETED
  # 5.) add all buttons in __create_Welcome_Window								COMPLETED
# Create 'update' method to update screen when values change 					COMPLETED
  # This method would be called 'refreshScreen'									COMPLETED

#===TODO===#
# Main GUI, make it more obvious what to do 									WIP
  # Replace 'Pacing Modes' label with 'Select a Pacing Mode'					COMPLETED
  # When pressing reset, ask the user to confirm 								COMPLETED
  # Prompt 'Do you want to save' when you change modes without saving			COMPLETED
  # Logout button
# Create more descriptive error messages										WIP
  # Having some issues in __check_In_Range function. Come back to this.			COMPLETED
  # If you save a value, it should be obvious that it was saved
# Serial comms b/w DCM and board
  # Transmit parameter and mode data
  # Conduct error checking
# Implement egram
# Show past 2 actions (save/reset)
  # Maybe have a window at the bottom, or have a 'log' file that saves all past actions

#===IMPORT===#
from tkinter import*
from tkinter import messagebox
from rw import*
from promptWindow import*

class Welcome():
	def __init__(self,screen): #Constructor, sets up inital values
		self.modeDict = {								#Dictionary to map modes to their code which tells the program which parameters are meaningful (1=meaningful)
			"Off":"0000000000000000000000000000000",
			"AAT":"1100000101010100110000000000000", 	# Not using
			"VVT":"1100000010101011000000000000000", 	# Not using
			"AOO":"1100000101010000000000000000000",
			"AAI":"1100000101010100110110000000000",
			"VOO":"1100000010101000000000000000000",
			"VVI":"1100000010101011000110000000000",
			"VDD":"1101110010101011001011111100000", 	# Not using
			"DOO":"1101000111111000000000000000000",
			"DDI":"1101000111111111110000000000000", 	# Not using
			"DDD":"1101111111111111111111111100000", 	# Not using
			"AOOR":"1110000101010000000000000001111",
			"AAIR":"1110000101010100110110000001111",
			"VOOR":"1110000010101000000000000001111",
			"VVIR":"1110000010101011000110000001111",
			"VDDR":"1111110010101011001011111111111", 	# Not using
			"DOOR":"1111000111111000000000000001111",
			"DDIR":"1111000111111111110000000001111", 	# Not using
			"DDDR":"1111111111111111111111111111111"  	# Not using
		}
		self.mode = "Off"

		# Ranges for each of the parameters
		self.lowerRateLimitRange = list(range(30,50,5))+list(range(50,90,1))+list(range(90,176,5)) 		#0
		self.upperRateLimitRange = list(range(50,176,5))												#1
		self.maxSensorRateRange = list(range(50,176,5))													#2
		self.fixedAVDelayRange = list(range(50,301,10))													#3
		self.dyanmicAVDelayRange = list(('OFF','ON'))													#4
		self.minDynamicAVDelayRange = list(range(30,101,10))											#5
		self.sensedAVDelayOffsetRange = list(('OFF',-10,-20,-30,-40,-50,-60,-70,-80,-90,-100))			#6
		self.avPulseAmpRegRange = list(('OFF',0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0)) #7,8
		self.avPulseAmpUnregRange = list(('OFF',1.25,2.5,3.75,5))																																#9,10
		self.avPulseWidthRange = list((0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9))																		#11,12
		self.aSensitivityRange = list((0.25,0.5,0.75))+list((1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10))																			#13
		self.vSensitivityRange = list((0.25,0.5,0.75))+list((1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10))																			#14
		self.VRPRange = list(range(150,510,10))															#15
		self.ARPRange = list(range(150,510,10))															#16
		self.pvarpRange = list(range(150,501,10))														#17
		self.pvarpExtensionRange = list(('OFF'))+list(range(50,401,50))									#18
		self.hysRange = ['OFF']+list(range(30,50,5))+list(range(50,90,1))+list(range(90,176,5))			#19
		self.rateSmoothingRange = list(('OFF',3,6,9,12,15,18,21,25))									#20
		self.atrFallBackModeRange = list(('OFF','ON'))													#24
		self.atrDurationCyclesRange = list(range(10,11,1))												#21
		self.atrDurationLowerRange = list(range(20,81,20))												#22
		self.atrDurationUpperRange = list(range(100,2001,100))											#23
		self.atrFallBackTimeRange = list(range(1,6,1))													#25
		self.ventricularBlankingRange = list(range(30,61,10))											#26
		self.activityThresholdRange = list(('V-LOW','LOW','MED-LOW','MED','MED-HIGH','HIGH','V-HIGH'))	#27
		self.reactionTimeRange = list(range(10,51,10))													#28
		self.responseFactorRange = list(range(1,17,1))													#29
		self.recoveryTimeRange = list(range(2,17,1))													#30
		self.rangesParam = list((self.lowerRateLimitRange,self.upperRateLimitRange,self.maxSensorRateRange,self.fixedAVDelayRange,self.dyanmicAVDelayRange,self.minDynamicAVDelayRange,
			self.sensedAVDelayOffsetRange,self.avPulseAmpRegRange,self.avPulseAmpRegRange,self.avPulseAmpUnregRange,self.avPulseAmpUnregRange,self.avPulseWidthRange,self.avPulseWidthRange,
			self.aSensitivityRange,self.vSensitivityRange,self.VRPRange,self.ARPRange,self.pvarpRange,self.pvarpExtensionRange,self.hysRange,self.rateSmoothingRange,self.atrDurationCyclesRange,
			self.atrDurationLowerRange,self.atrDurationUpperRange,self.atrFallBackModeRange,self.atrFallBackTimeRange,self.ventricularBlankingRange,self.activityThresholdRange,
			self.reactionTimeRange,self.responseFactorRange,self.recoveryTimeRange)) 					# Combining all ranges into a list

		self.parameterNamesParam = ["Lower Rate Limit","Upper Rate Limit","Maximum Sensor Rate","Fixed AV Delay","Dynamic AV Delay","Minimum Dynamic AV Delay",
		"Sensed AV Delay Offset","Atrial Pulse Amplitude Regulated","Ventricular Pulse Amplitude Regulated","Atrial Pulse Amplitude Unregulated",
		"Ventricular Pulse Amplitude Unregulated","Atrial Pulse Width","Ventricular Pulse Width","Atrial Sensitivity","Ventricular Sensitivity",
		"Ventricular Regulatory Pulse","Atrial Regulatory Pulse","PVARP","PVARP Extension","Hysteresis","Rate Smoothing","Atrial Fallback Mode",
		"Atrial Duration Cycles","Atrial Duration Lower Range","Atrial Duration Upper Range","Ventricular Blanking","Atrial Fall Back Time","Activity Threshold",
		"Reaction Time","Response Factor","Recovery Time"]

		self.progParam = []

		self.numParams = 31
		self.labelParams = [None]*self.numParams
		self.spinboxParams = [None]*self.numParams
		self.commsStatus = 1 # 0 means good status
		self.boardStatus = 1 # 0 means good board
		self.spinboxBD = 2
		self.root = screen
		self.commsStatusInd = StringVar()
		self.commsStatusInd.set(self.__get_Comms_Status())
		self.boardStatusInd = StringVar()
		self.boardStatusInd.set(self.__get_Board_Status())

		self.__get_User_Data()
		self.__create_Welcome_Window()

		self.root.mainloop() #All statements must occur before this line as .mainloop() traps it for all eternity. (.mainloop ~ while(1))

	def __get_Comms_Status(self): # Gets comms status. Currently psuedo code - will call upon an external class in the future
		if(self.commsStatus==0):
			return "GOOD"
		else:
			return "BAD"

	def __get_Board_Status(self): # Gets board status. Currently psuedo code - will call upon an external class in the future
		if(self.boardStatus==0):
			return "GOOD"
		else:
			return "BAD"

	def __get_User_Data(self): # Gets programmable parameters from rw class
		file=RW()
		self.progParam=file.get_ProgParam(0)

	def __set_User_Data(self): # Sets user data by sending self.progParam to rw class
		file = RW()
		file.set_ProgParam(self.progParam)

	def __get_Default_Values(self,mode): # Gets default nominal values from rw class instead of primary user values. Has the option of reading default for all parameters, or just for 1 mode
		file=RW()						 # if code = -1, set all values to default, if not, only set 1 modes' values to default
		if(mode==-1):
			self.progParam=file.get_ProgParam(1)
		else:
			self.progParam[mode]=file.get_ProgParam(1)[mode]

	def __confirm_Reset_Default_Values(self):
		confirmReset = Tk()
		confirmReset.title("Are you sure?")

		def __confirmed(window):
			window.destroy()
			self.__set_Default_Values()

		Label(confirmReset,text="Are you sure you want to reset to nominal values?").pack()
		Button(confirmReset,text="Yes, reset to nominal values.",command=lambda:__confirmed(confirmReset)).pack(fill=X)
		Button(confirmReset,text="No, return to editor.",command=confirmReset.destroy).pack(fill=X)

	def __set_Default_Values(self): # Sets default nominal values for one mode by using the rw class
		self.__get_Default_Values(self.__mode_Enum())
		self.__set_User_Data()
		self.__refresh_Screen()
	
	def __save_Param(self): # Saves the data currently in spinboxes by reading all data, checking if its in range then finally calling the __set_User_Data() function 
		if(self.__check_In_Range()==0): # If the data is bad, it displays an error and reset the spinboxes to what they were at before
			self.__get_Vals()
			self.__set_User_Data()
		else:
			self.__refresh_Screen()

	def __refresh_Screen(self):
		self.__show_MODE(self.mode)

	def __get_Vals(self): # Saves relevant spinbox data into self.progParam depending on what pacing mode the user is editing
		index = 0

		for get in self.modeDict[self.mode]:
			if(get == '1'):
				self.progParam[self.__mode_Enum()][index] = self.spinboxParams[index].get()
			index+=1

	def __check_In_Range(self): # Checks if the current data stored in the spinboxes is valid. NOTE: Checks spinboxes and NOT self.progParam as we don't want to potentially overwrite good data with bad data
		index = 0

		print("Checking for valid values in mode: "+self.mode)
		for check in self.modeDict[self.mode]:
			if(check == '1'):
				print("check int for "+self.parameterNamesParam[index])
				try:
					if((int(self.spinboxParams[index].get()) in self.rangesParam[index]) == 0):
						# print("1Data out of Range"+"Entered value of "+self.spinboxParams[index].get()+" not in allowed range of "+self.rangesParam[index]+"!")
						# messagebox.showerror("Out of range! Possible values below.",self.rangesParam[index])
						promptWindow5("Data out of Range","Entered value:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
						return 1
				except:
					print("check float for "+self.parameterNamesParam[index])
					try:
						if((float(self.spinboxParams[index].get()) in self.rangesParam[index]) == 0):
							# print("2Data out of Range"+"Entered value of "+self.spinboxParams[index].get()+" not in allowed range of "+self.rangesParam[index]+"!")
							# messagebox.showerror("Out of range! Possible values below.",self.rangesParam[index])
							promptWindow5("Data out of Range","Entered value:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
							return 1
					except:
						print("check string for "+self.parameterNamesParam[index])
						try:
							if((self.spinboxParams[index].get() in self.rangesParam[index]) == 0):
								# print("3Data out of Range"+"Entered value of "+self.spinboxParams[index].get()+" not in allowed range of "+self.rangesParam[index]+"!")
								# messagebox.showerror("Out of range! Possible values below.",self.rangesParam[index])
								promptWindow5("Data out of Range","Entered values:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
								return 1
						except:
							# messagebox.showerror("Out of range! Possible values below.",self.rangesParam[index])
							promptWindow5("Data out of Range","Entered value:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
							return 1
			index+=1

		return 0

	def __check_If_Same(self): # returns 0 if spinbox values match stored. returns 1 else
		index = 0
		print("Checking for unsaved values in "+self.mode)
		for check in self.modeDict[self.mode]:
			if(check == '1'):
				if(self.progParam[self.__mode_Enum()][index] != self.spinboxParams[index].get()):
					return 1

			# 	print("Checking index "+str(index)+", Comparing to: "+self.progParam[self.__mode_Enum()][index])
			# 	print("Spinbox value: "+self.spinboxParams[index].get())
				# print(self.progParam[self.__mode_Enum()][index] == self.spinboxParams[index].get())
			index+=1

		return 0

	def __mode_Enum(self):
		if(self.mode == "Off"):
			return -1
		if(self.mode == "AAT"):
			return 0
		if(self.mode == "VVT"):
			return 1
		if(self.mode == "AOO"):
			return 2
		if(self.mode == "AAI"):
			return 3
		if(self.mode == "VOO"):
			return 4
		if(self.mode == "VVI"):
			return 5
		if(self.mode == "VDD"):
			return 6
		if(self.mode == "DOO"):
			return 7
		if(self.mode == "DDI"):
			return 8
		if(self.mode == "DDD"):
			return 9
		if(self.mode == "AOOR"):
			return 10
		if(self.mode == "AAIR"):
			return 11
		if(self.mode == "VOOR"):
			return 12
		if(self.mode == "VVIR"):
			return 13
		if(self.mode == "VDDR"):
			return 14
		if(self.mode == "DOOR"):
			return 15
		if(self.mode == "DDIR"):
			return 16
		if(self.mode == "DDDR"):
			return 17

	def __show_MODE(self,mode): # Displays the correct labels, spinboxes, and activates/deactivates the save/reset buttons
		# If values different from stored, confirm if they want to switch
		self.mode = mode

		index = 0

		for show in self.modeDict[self.mode]:
			self.labelParams[index].pack_forget()
			self.spinboxParams[index].pack_forget()
			index+=1

		index = 0

		for show in self.modeDict[self.mode]:
			if(int(show)):
				self.labelParams[index].pack(side=TOP,fill=X,expand=False)
				self.spinboxParams[index].pack(side=TOP,fill=X,expand=False)
			else:
				self.labelParams[index].pack_forget()
				self.spinboxParams[index].pack_forget()
			index+=1

		index = 0

		for show in self.modeDict[self.mode]:
			if(int(show)):
				self.spinboxParams[index].delete(0,"end")
				self.spinboxParams[index].insert(0,self.progParam[self.__mode_Enum()][index])
			index+=1

		if(self.__mode_Enum() == -1):
			self.but_Save.config(state=DISABLED)
			self.but_Reset.config(state=DISABLED)
		else:
			self.but_Save.config(state=NORMAL)
			self.but_Reset.config(state=NORMAL)

		self.but_Off.config(relief='raised')
		self.but_AOO.config(relief='raised')
		self.but_VOO.config(relief='raised')
		self.but_AAI.config(relief='raised')
		self.but_VVI.config(relief='raised')
		self.but_DOO.config(relief='raised')
		self.but_AOOR.config(relief='raised')
		self.but_AAIR.config(relief='raised')
		self.but_VOOR.config(relief='raised')
		self.but_VVIR.config(relief='raised')
		self.but_DOOR.config(relief='raised')
		
		if(self.__mode_Enum() == -1):
			self.but_Off.config(relief='sunken')
		elif(self.__mode_Enum() == 2):
			self.but_AOO.config(relief='sunken')
		elif(self.__mode_Enum() == 3):
			self.but_AAI.config(relief='sunken')
		elif(self.__mode_Enum() == 4):
			self.but_VOO.config(relief='sunken')
		elif(self.__mode_Enum() == 5):
			self.but_VVI.config(relief='sunken')
		elif(self.__mode_Enum() == 7):
			self.but_DOO.config(relief='sunken')
		elif(self.__mode_Enum() == 10):
			self.but_AOOR.config(relief='sunken')
		elif(self.__mode_Enum() == 11):
			self.but_AAIR.config(relief='sunken')
		elif(self.__mode_Enum() == 12):
			self.but_VOOR.config(relief='sunken')
		elif(self.__mode_Enum() == 13):
			self.but_VVIR.config(relief='sunken')
		elif(self.__mode_Enum() == 15):
			self.but_DOOR.config(relief='sunken')

	def __edit_MODE(self,mode): # Checks if unsaved errors exist. If so, prompt user to go back and save or ignore. Calls __show_MODE(,) to actually view the mode
		if(self.__check_If_Same() == 1):
			# Confirm w/ user
			confirmDoNotSave = Tk()
			confirmDoNotSave.title("Are you sure?")

			def __confirmed(window):
				window.destroy()
				self.__show_MODE(mode);

			Label(confirmDoNotSave,text="There are unsaved changes. Do you want to go back and save?").pack()
			Button(confirmDoNotSave,text="Yes, go back and save changes.",command=confirmDoNotSave.destroy).pack(fill=X)
			Button(confirmDoNotSave,text="No, switch modes and delete changes.",command=lambda:__confirmed(confirmDoNotSave)).pack(fill=X)
		else:
			self.__show_MODE(mode)

	def __create_Welcome_Window(self): # Creates the main GUI using .pack()
		self.root.title("DCM")
		self.root.geometry("500x500+100+100")
		
		self.metaDataFrame = Frame(self.root,bg="grey50",bd=4)
		self.metaDataFrame.pack(side = TOP,fill=X,expand=False)
		self.Ind11 = Label(self.metaDataFrame, text="Communication Status: ",bg="grey50",fg="snow")
		self.Ind11.pack(side=LEFT)
		self.Ind12 = Label(self.metaDataFrame, textvariable=self.commsStatusInd,bg="grey50",fg="snow")
		self.Ind12.pack(side = LEFT)
		self.Ind21 = Label(self.metaDataFrame, text="Board Status: ",bg="grey50",fg="snow")
		self.Ind21.pack(side=LEFT)
		self.Ind22 = Label(self.metaDataFrame, textvariable=self.boardStatusInd,bg="grey50",fg="snow")
		self.Ind22.pack(side = LEFT)

		self.otherFrame = Frame(self.root,bg="yellow")
		self.otherFrame.pack(side = BOTTOM,fill=BOTH,expand=True)

		#===Pacing mode selection explorer===#
		self.pacingModesFrame = Frame(self.otherFrame,bg="gainsboro")
		self.pacingModesFrame.pack(side = LEFT,fill=Y,expand=False)
		self.pacingModesLabel = Label(self.pacingModesFrame,text="Select a Pacing Mode",justify=LEFT,bg="gainsboro",fg="black")
		self.pacingModesLabel.pack(side=TOP)
		self.but_Off = Button(self.pacingModesFrame,text="Off",bg="snow",fg="black",command=lambda:self.__edit_MODE("Off"))
		self.but_Off.pack(side=TOP,fill=X)
		self.but_AOO = Button(self.pacingModesFrame,text="AOO",bg="snow",fg="black",command=lambda:self.__edit_MODE("AOO"))
		self.but_AOO.pack(side=TOP,fill=X)
		self.but_VOO = Button(self.pacingModesFrame,text="VOO",bg="snow",fg="black",command=lambda:self.__edit_MODE("VOO"))
		self.but_VOO.pack(side=TOP,fill=X)
		self.but_AAI = Button(self.pacingModesFrame,text="AAI",bg="snow",fg="black",command=lambda:self.__edit_MODE("AAI"))
		self.but_AAI.pack(side=TOP,fill=X)
		self.but_VVI = Button(self.pacingModesFrame,text="VVI",bg="snow",fg="black",command=lambda:self.__edit_MODE("VVI"))
		self.but_VVI.pack(side=TOP,fill=X)
		self.but_DOO = Button(self.pacingModesFrame,text="DOO",bg="snow",fg="black",command=lambda:self.__edit_MODE("DOO"))
		self.but_DOO.pack(side=TOP,fill=X)
		self.but_AOOR = Button(self.pacingModesFrame,text="AOOR",bg="snow",fg="black",command=lambda:self.__edit_MODE("AOOR"))
		self.but_AOOR.pack(side=TOP,fill=X)
		self.but_AAIR = Button(self.pacingModesFrame,text="AAIR",bg="snow",fg="black",command=lambda:self.__edit_MODE("AAIR"))
		self.but_AAIR.pack(side=TOP,fill=X)
		self.but_VOOR = Button(self.pacingModesFrame,text="VOOR",bg="snow",fg="black",command=lambda:self.__edit_MODE("VOOR"))
		self.but_VOOR.pack(side=TOP,fill=X)
		self.but_VVIR = Button(self.pacingModesFrame,text="VVIR",bg="snow",fg="black",command=lambda:self.__edit_MODE("VVIR"))
		self.but_VVIR.pack(side=TOP,fill=X)
		self.but_DOOR = Button(self.pacingModesFrame,text="DOOR",bg="snow",fg="black",command=lambda:self.__edit_MODE("DOOR"))
		self.but_DOOR.pack(side=TOP,fill=X)

		#===Parameter explorer===#
		self.progParamFrame = Frame(self.otherFrame,bg="black")
		self.progParamFrame.pack(side = RIGHT,fill=BOTH,expand=True)

		#===Description===#
		self.progParamFrameTop = Frame(self.progParamFrame,bg="gainsboro")
		self.progParamFrameTop.pack(side=TOP,fill=X,expand=False)
		self.progParamFrameLabel = Label(self.progParamFrameTop,text="Edit Parameters",justify=LEFT,bg="gainsboro",fg="black")
		self.progParamFrameLabel.pack()

		#===Save & Reset Actions===#
		self.progParamFrameActions = Frame(self.progParamFrame,bg="snow")
		self.progParamFrameActions.pack(side=BOTTOM,fill=X,expand=False)
		self.but_Save = Button(self.progParamFrameActions,text="Save Parameters",state=DISABLED,command=self.__save_Param,bg="snow",fg="black")
		self.but_Save.pack(side=LEFT)
		self.but_Reset = Button(self.progParamFrameActions,text="Reset parameters to nominal",state=DISABLED,command=self.__confirm_Reset_Default_Values,bg="snow",fg="black")
		self.but_Reset.pack(side=LEFT)

		#===Parameter labels===#
		self.progParamFrameItemsL = Frame(self.progParamFrame,bg="snow")
		self.progParamFrameItemsL.pack(side=LEFT,fill=Y,expand=False)
		self.labelParams[0] = Label(self.progParamFrameItemsL,text="Lower Rate Limit: ",justify=LEFT,bg="snow")
		self.labelParams[1] = Label(self.progParamFrameItemsL,text="Upper Rate Limit: ",justify=LEFT,bg="snow")
		self.labelParams[2] = Label(self.progParamFrameItemsL,text="Maximum Sensor Rate: ",justify=LEFT,bg="snow")
		self.labelParams[3] = Label(self.progParamFrameItemsL,text="Fixed AV Delay: ",justify=LEFT,bg="snow")
		
		self.labelParams[4] = Label(self.progParamFrameItemsL,text="Dynamic AV Delay: ",justify=LEFT,bg="snow")
		self.labelParams[5] = Label(self.progParamFrameItemsL,text="Minimum Dynamic AV Delay: ",justify=LEFT,bg="snow")
		self.labelParams[6] = Label(self.progParamFrameItemsL,text="Sensed AV Delay Offset: ",justify=LEFT,bg="snow")
		self.labelParams[7] = Label(self.progParamFrameItemsL,text="Atrial Pulse Amplitude Reg.: ",justify=LEFT,bg="snow")
		
		self.labelParams[8] = Label(self.progParamFrameItemsL,text="Ventricular Pulse Amplitude Reg.: ",justify=LEFT,bg="snow")
		self.labelParams[9] = Label(self.progParamFrameItemsL,text="Atrial Pulse Amplitude Unreg.: ",justify=LEFT,bg="snow")
		self.labelParams[10] = Label(self.progParamFrameItemsL,text="Ventricular Pulse Amplitude Unreg.: ",justify=LEFT,bg="snow")
		self.labelParams[11] = Label(self.progParamFrameItemsL,text="Atrial Pulse Width: ",justify=LEFT,bg="snow")
		
		self.labelParams[12] = Label(self.progParamFrameItemsL,text="Ventricular Pulse Width: ",justify=LEFT,bg="snow")
		self.labelParams[13] = Label(self.progParamFrameItemsL,text="Atrial Sensitivity: ",justify=LEFT,bg="snow")
		self.labelParams[14] = Label(self.progParamFrameItemsL,text="Ventricular Sensitivity: ",justify=LEFT,bg="snow")
		self.labelParams[15] = Label(self.progParamFrameItemsL,text="Venrticular Refractory Period: ",justify=LEFT,bg="snow")
		
		self.labelParams[16] = Label(self.progParamFrameItemsL,text="Atrial Refractory Period: ",justify=LEFT,bg="snow")
		self.labelParams[17] = Label(self.progParamFrameItemsL,text="PVARP: ",justify=LEFT,bg="snow")
		self.labelParams[18] = Label(self.progParamFrameItemsL,text="PVARP Extension: ",justify=LEFT,bg="snow")
		self.labelParams[19] = Label(self.progParamFrameItemsL,text="Hysteresis: ",justify=LEFT,bg="snow")
		
		self.labelParams[20] = Label(self.progParamFrameItemsL,text="Rate Smoothing: ",justify=LEFT,bg="snow")
		self.labelParams[21] = Label(self.progParamFrameItemsL,text="ATR Duration Cycles: ",justify=LEFT,bg="snow")
		self.labelParams[22] = Label(self.progParamFrameItemsL,text="ATR Duration Lower Range: ",justify=LEFT,bg="snow")
		self.labelParams[23] = Label(self.progParamFrameItemsL,text="ATR Duration Upper Range: ",justify=LEFT,bg="snow")
		
		self.labelParams[24] = Label(self.progParamFrameItemsL,text="ATR Fallback Mode: ",justify=LEFT,bg="snow")
		self.labelParams[25] = Label(self.progParamFrameItemsL,text="ATR Fallback Time: ",justify=LEFT,bg="snow")
		self.labelParams[26] = Label(self.progParamFrameItemsL,text="Ventricular Blanking: ",justify=LEFT,bg="snow")
		self.labelParams[27] = Label(self.progParamFrameItemsL,text="Activity Threshold: ",justify=LEFT,bg="snow")
		
		self.labelParams[28] = Label(self.progParamFrameItemsL,text="Reaction Time: ",justify=LEFT,bg="snow")
		self.labelParams[29] = Label(self.progParamFrameItemsL,text="Response Factor: ",justify=LEFT,bg="snow")
		self.labelParams[30] = Label(self.progParamFrameItemsL,text="Recovery Time: ",justify=LEFT,bg="snow")

		#===Parameter Spinboxes===#
		self.progParamFrameItemsR = Frame(self.progParamFrame,bg="snow")
		self.progParamFrameItemsR.pack(side=LEFT,fill=BOTH,expand=True)
		self.spinboxParams[0] = Spinbox(self.progParamFrameItemsR,values=self.lowerRateLimitRange,bd=self.spinboxBD)
		self.spinboxParams[1] = Spinbox(self.progParamFrameItemsR,values=self.upperRateLimitRange,bd=self.spinboxBD)
		self.spinboxParams[2] = Spinbox(self.progParamFrameItemsR,values=self.maxSensorRateRange,bd=self.spinboxBD)
		self.spinboxParams[3] = Spinbox(self.progParamFrameItemsR,values=self.fixedAVDelayRange,bd=self.spinboxBD)
		
		self.spinboxParams[4] = Spinbox(self.progParamFrameItemsR,values=self.dyanmicAVDelayRange,bd=self.spinboxBD)
		self.spinboxParams[5] = Spinbox(self.progParamFrameItemsR,values=self.minDynamicAVDelayRange,bd=self.spinboxBD)
		self.spinboxParams[6] = Spinbox(self.progParamFrameItemsR,values=self.sensedAVDelayOffsetRange,bd=self.spinboxBD)
		self.spinboxParams[7] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpRegRange,bd=self.spinboxBD)
		
		self.spinboxParams[8] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpRegRange,bd=self.spinboxBD)
		self.spinboxParams[9] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpUnregRange,bd=self.spinboxBD)
		self.spinboxParams[10] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpUnregRange,bd=self.spinboxBD)
		self.spinboxParams[11] = Spinbox(self.progParamFrameItemsR,values=self.avPulseWidthRange,bd=self.spinboxBD)
		
		self.spinboxParams[12] = Spinbox(self.progParamFrameItemsR,values=self.avPulseWidthRange,bd=self.spinboxBD)
		self.spinboxParams[13] = Spinbox(self.progParamFrameItemsR,values=self.aSensitivityRange,bd=self.spinboxBD)
		self.spinboxParams[14] = Spinbox(self.progParamFrameItemsR,values=self.vSensitivityRange,bd=self.spinboxBD)
		self.spinboxParams[15] = Spinbox(self.progParamFrameItemsR,values=self.VRPRange,bd=self.spinboxBD)
		
		self.spinboxParams[16] = Spinbox(self.progParamFrameItemsR,values=self.ARPRange,bd=self.spinboxBD)
		self.spinboxParams[17] = Spinbox(self.progParamFrameItemsR,values=self.pvarpRange,bd=self.spinboxBD)
		self.spinboxParams[18] = Spinbox(self.progParamFrameItemsR,values=self.pvarpExtensionRange,bd=self.spinboxBD)
		self.spinboxParams[19] = Spinbox(self.progParamFrameItemsR,values=self.hysRange,bd=self.spinboxBD)
		
		self.spinboxParams[20] = Spinbox(self.progParamFrameItemsR,values=self.rateSmoothingRange,bd=self.spinboxBD)
		self.spinboxParams[21] = Spinbox(self.progParamFrameItemsR,values=self.atrDurationCyclesRange,bd=self.spinboxBD)
		self.spinboxParams[22] = Spinbox(self.progParamFrameItemsR,values=self.atrDurationLowerRange,bd=self.spinboxBD)
		self.spinboxParams[23] = Spinbox(self.progParamFrameItemsR,values=self.atrDurationUpperRange,bd=self.spinboxBD)
		
		self.spinboxParams[24] = Spinbox(self.progParamFrameItemsR,values=self.atrFallBackModeRange,bd=self.spinboxBD)
		self.spinboxParams[25] = Spinbox(self.progParamFrameItemsR,values=self.atrFallBackTimeRange,bd=self.spinboxBD)
		self.spinboxParams[26] = Spinbox(self.progParamFrameItemsR,values=self.ventricularBlankingRange,bd=self.spinboxBD)
		self.spinboxParams[27] = Spinbox(self.progParamFrameItemsR,values=self.activityThresholdRange,bd=self.spinboxBD)

		self.spinboxParams[28] = Spinbox(self.progParamFrameItemsR,values=self.reactionTimeRange,bd=self.spinboxBD)
		self.spinboxParams[29] = Spinbox(self.progParamFrameItemsR,values=self.responseFactorRange,bd=self.spinboxBD)
		self.spinboxParams[30] = Spinbox(self.progParamFrameItemsR,values=self.recoveryTimeRange,bd=self.spinboxBD)

		self.but_Off.config(relief='sunken')