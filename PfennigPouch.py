from decimal import Decimal
import PySimpleGUI as sg
import logging    
import traceback
import os
cwd = os.getcwd()

sg.theme('DarkAmber')    # Keep things interesting for your users

def PocketChange(gold=False, silver=False, copper=False, option:str="straight",golddec=2,silverdec=1,copperdec=0,forceRoundDown=True, debug=False):
    '''
    Receives inputs of values and returns the amount for each individual type as a total pile, has three options: Straight convert, Round to gold, Round to silver, and control the amount of decimal places in
    in each option. Can also choose if the function forces itself to half round down or half round up (5 is rounded up)
    '''

        
    def OutputFormatter(value,decimalPlaces:int,forceRoundDown=forceRoundDown):
        # value = 2.456 , decimalplaces = 2, forceround down = True 
        # expects 2.45
        if forceRoundDown != True:
            return(round(value,decimalPlaces))
        
        #convertFactor = 10 ** decimalPlaces # 100
        
        # 2.456
        result = value * (10 ** decimalPlaces)
        
        #245.6
        decimalstrip = result % int(1) # 0.55999999999999943
        result = result - decimalstrip
        
        #245
        result = result/(10 ** decimalPlaces)
        #2.45
        
        

        return(result)

    def CoinConverter (gold=gold, silver=silver, copper=copper, option=option, golddec=golddec,silverdec=silverdec,copperdec=copperdec,debug=debug):  #!hyperstraight function (or is it?)
        """
            Receives inputs of values and returns the amount for each individual type as a total pile, has three functions: Straight convert, Round to gold, Round to silver(pocketchange)
        """
        print(golddec,silverdec,copperdec)   #!debug printout
        inputCopper = copper # 0 copper 
        inputCopper += silver*12 # 20 silver = 240 copper
        inputCopper += gold*240  # still 240 copper
        
        
        outputgold = OutputFormatter(inputCopper/240,golddec) # converts copper to gold (change second variable to adjust output decimal places)
        outputsilver = OutputFormatter(inputCopper/12,silverdec) # converts copper to silver (change second variable to adjust output decimal places)
        outputcopper = OutputFormatter(inputCopper,copperdec) # outputs copper (change second variable to adjust output decimal places)
        
        if option == "rtg":
            
            outputgold = int(inputCopper / 240) 
            inputCopper = inputCopper - (outputgold * 240) #turns as much copper to gold as possible, then outputs amount of copper left after gold is converted
            
            outputsilver = int(inputCopper / 12) #turns the remaining copper into as much silver as possible
            outputcopper = inputCopper - (outputsilver * 12)#the amount of copper remaining after silver
            
            print("rtg",outputgold, outputsilver, outputcopper)
            return(outputgold, outputsilver, outputcopper)
        
        if option == "rts":
            
            outputsilver = int(inputCopper / 12) #turns all copper to silver
            outputcopper = inputCopper - (silver * 12) #outputs remaining copper
            
            print("rts",outputgold, outputsilver, outputcopper)
            return(int(outputgold), int(outputsilver), int(outputcopper))

            #todo 4th option is spending tracker
                #todo requires new input function to process "current funds" to output instead of translating

        
        # elif option != "Straight" or "straight" or "rtg" or "rts":
        #     return(print("Invalid option","***"+str(option)+"***"))
        
        #result = (f"{outputgold:.{golddec}f}",f"{outputsilver:.{golddec}f}",f"{outputcopper:.{golddec}f}")
        result = (outputgold,outputsilver,outputcopper)
        return (result)

    gold,silver,copper = CoinConverter(gold,silver,copper)
    result = (f"{gold:.{golddec}f}",f"{silver:.{silverdec}f}",f"{copper:.{copperdec}f}")
    if debug ==True:
        print (result)
        return(result)
    return(result)


b1 = [[sg.Column([
    #"Gold: " + str(GOLD1)+ " | " + "Silver: " + str(SILVER20)+  " | " + "Copper: " + str(COPPER240)
    [sg.Push(),sg.Text("", key="-Dialogue-", text_color="#fdc3a2"),sg.Push()],
    
    [sg.Input(key='-G-', size= (9,10),enable_events = True,justification="c", default_text = "G", expand_x = True),sg.Input(key='-S-', size= (9,10),enable_events = True,justification="c", default_text = "S", expand_x = True),sg.Input(key='-C-', size= (9,10),enable_events = True,justification="c", default_text = "C", expand_x = True)],

    [sg.Button("Clear"),sg.Push(),sg.OptionMenu(values=("   Straight","Round to Gold","Round to Silver"), key="type1", default_value="   Straight",),sg.Push(),sg.Exit()]

    
    ],pad=(5,(5,5)))]]

c1 = [sg.Frame(layout=b1,title="◆──◇─◆ Pfennig Pouch ◆─◇──◆", pad= (1,(1,10)),border_width = (1),title_location=sg.TITLE_LOCATION_TOP)]
layout = [c1]

window = sg.Window("Pfennig Pouch",
                    layout,
                    text_justification='c',
                    no_titlebar=True,
                    grab_anywhere=True,
                    keep_on_top=True, finalize=True,font=("ink free", "14", "bold"))
window['type1'].Widget.configure(justify='center',)
window['-G-'].bind('<Button-1>','+CLICKEDG') 
window['-S-'].bind('<Button-1>','+CLICKEDS') 
window['-C-'].bind('<Button-1>','+CLICKEDC') 

#region
while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)   

    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event.endswith('+CLICKEDG'):
        window['-G-'].update(select=True)
    if event.endswith('+CLICKEDS'):
        window['-S-'].update(select=True)
    if event.endswith('+CLICKEDC'):
        window['-C-'].update(select=True)

    if values["type1"] == "   Straight": #***Straight
            
        if event == "-G-": #*GOLD STRAIGHT
            if len(values['-G-']) and values['-G-'][-1] not in ('0123456789.'):
                window['-G-'].update(values['-G-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
                
            try:
                
                    window["-Dialogue-"](value="")
                    window["-S-"](value="S")
                    window["-C-"](value="C")
                
                    MoneyBag = PocketChange(gold=Decimal(values['-G-']),golddec=0,silverdec=0,debug=True) #! I thnk it's this int that's actually causing the problem, but I don't see a way to get rid of it
                    print ("pocketchange outputlist",MoneyBag)
                    Gold,Silver,Copper = MoneyBag
                    print ("moneybag unpack",Gold,Silver,Copper)
                    window["-Dialogue-"](value= "Gold: " + str(Gold)+ "  |  " + "Silver: " + str(Silver)+  "  |  " + "Copper: " + str(Copper))
                    
                    
            except BaseException:
                logging.exception("*oh no, an error D:*")   
 
                        
        if event == "-S-": #*SILVER STRAIGHT
            if len(values['-S-']) and values['-S-'][-1] not in ('0123456789.'):
    
                window['-S-'].update(values['-S-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
                
            try:
                window["-Dialogue-"](value="")
                window["-G-"](value="G")
                window["-C-"](value="C")
                
                MoneyBag = PocketChange(silver=Decimal(values['-S-']),golddec=2,silverdec=0,debug=True)
                Gold,Silver,Copper = MoneyBag
                
                window["-Dialogue-"](value= "Gold: " + str(Gold) + "  |  " + "Silver: " + str(Silver)+  "  |  " + "Copper: " + str(Copper))
            except BaseException:
                logging.exception("*oh no, an error D:*")   

        if event == "-C-": #*COPPER STRAIGHT
            if len(values['-C-']) and values['-C-'][-1] not in ('0123456789.'):
    
                window['-C-'].update(values['-C-'][:-1])
            try:
                
                window["-Dialogue-"](value="")
                window["-G-"](value="G")
                window["-S-"](value="S")

                MoneyBag = PocketChange(copper=Decimal(values['-C-']),golddec=2,silverdec=2,debug=True,forceRoundDown=False)
                
                Gold,Silver,Copper = MoneyBag
                

                window["-Dialogue-"](value= "Gold: " + str(Gold)+ " | " + "Silver: " + str(Silver)+  " | " + "Copper: " + str(Copper))
            except BaseException:
                logging.exception("*oh no, an error D:*")   
                if values["-C-"] != "" or " " or "C":
                    window["-Dialogue-"](value="Numbers only!")
        if event == "Clear":
            window["-G-"](value="G")
            window["-S-"](value="S")
            window["-C-"](value="C")
            window["-Dialogue-"]("")    
            
    #*#############################################################################################*#
    
    if values["type1"] == "Round to Gold": #***Round to Gold
        window['-Dialogue-']("") 
        if event == "-G-": #*GOLD RTGOLD
            if len(values['-G-']) and values['-G-'][-1] not in ('0123456789.'):
    
                window['-G-'].update(values['-G-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
            try:
                
                    window["-Dialogue-"](value="")
                    window["-S-"](value="S")
                    window["-C-"](value="C")
                
                    MoneyBag = PocketChange(gold=Decimal(values['-G-']),golddec=0,silverdec=0,option="rtg",debug=True)
                    print ("pocketchange outputlist",MoneyBag)
                    Gold,Silver,Copper = MoneyBag
                    print ("moneybag unpack",Gold,Silver,Copper)
                    window["-Dialogue-"](value= "Gold: " + str(Gold)+ "    " + "Silver: " + str(Silver)+  "/- " +str(Copper) + "c " )
                    
                    
            except BaseException:
                logging.exception("*oh no, an error D:*")   
                
        if event == "-S-": #*SILVER RTGOLD
            if len(values['-S-']) and values['-S-'][-1] not in ('0123456789.'):
    
                window['-S-'].update(values['-S-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
                
                
            try:
                window["-Dialogue-"](value="")
                window["-G-"](value="G")
                window["-C-"](value="C")
                
                MoneyBag = PocketChange(silver=Decimal(values['-S-']),golddec=0,silverdec=0,option="rtg",debug=True)
                Gold,Silver,Copper = MoneyBag
                
                window["-Dialogue-"](value= "Gold: " + str(Gold)+ "    " + "Silver: " + str(Silver)+  "/- " +str(Copper) + "c " )
            except BaseException:
                logging.exception("*oh no, an error D:*")                

        if event == "-C-": #*COPPER RTGOLD
            if len(values['-C-']) and values['-C-'][-1] not in ('0123456789.'):
    
                window['-C-'].update(values['-C-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
            try:
                
                window["-Dialogue-"](value="")
                window["-G-"](value="G")
                window["-S-"](value="S")

                MoneyBag = PocketChange(copper=Decimal(values['-C-']),golddec=0,silverdec=0,debug=True,option="rtg",forceRoundDown=False)
                
                Gold,Silver,Copper = MoneyBag
                

                window["-Dialogue-"](value= "Gold: " + str(Gold)+ "    " + "Silver: " + str(Silver)+  "/- " +str(Copper) + "c " )
            except BaseException:
                logging.exception("*oh no, an error D:*") 

        if event == "Clear":
            window["-G-"](value="G")
            window["-S-"](value="S")
            window["-C-"](value="C")
            window["-Dialogue-"]("")   
    
    
    
    else:
        logging.exception("Error")
        print(traceback.format_exc())
        
    #*#############################################################################################*#
    
    if values["type1"] == "Round to Silver": #***Round to Silver
            
        if event == "-G-": #*GOLD RTSILVER
            if len(values['-G-']) and values['-G-'][-1] not in ('0123456789.'):
    
                window['-G-'].update(values['-G-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
            try:
                
                    window["-Dialogue-"](value="")
                    window["-S-"](value="S")
                    window["-C-"](value="C")
                
                    MoneyBag = PocketChange(gold=Decimal(values['-G-']),golddec=0,silverdec=0,option="rts",debug=True)
                    print ("pocketchange outputlist",MoneyBag)
                    Gold,Silver,Copper = MoneyBag
                    print ("moneybag unpack",Gold,Silver,Copper)
                    window["-Dialogue-"](+ "Silver: " + str(Silver)+  "/- " +str(Copper) + "c " )
                    
                    
            except BaseException:
                logging.exception("*oh no, an error D:*")   
                
        if event == "-S-": #*SILVER RTSILVER
            if len(values['-S-']) and values['-S-'][-1] not in ('0123456789.'):
    
                window['-S-'].update(values['-S-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
                
                
            try:
                window["-Dialogue-"](value="")
                window["-G-"](value="G")
                window["-C-"](value="C")
                
                MoneyBag = PocketChange(silver=Decimal(values['-S-']),golddec=0,silverdec=0,option="rts",debug=True)
                Gold,Silver,Copper = MoneyBag
                
                window["-Dialogue-"](value= "Silver: " + str(Silver)+  "/- " +str(Copper) + "c " )
            except BaseException:
                logging.exception("*oh no, an error D:*")                

        if event == "-C-": #*COPPER RTSILVER
            if len(values['-C-']) and values['-C-'][-1] not in ('0123456789.'):
    
                window['-C-'].update(values['-C-'][:-1])
                window["-Dialogue-"](value="Numbers only!")  
            try:
                
                window["-Dialogue-"](value="")
                window["-G-"](value="G")
                window["-S-"](value="S")

                MoneyBag = PocketChange(copper=Decimal(values['-C-']),golddec=0,silverdec=0,debug=True,option="rts",forceRoundDown=False)
                
                Gold,Silver,Copper = MoneyBag
                

                window["-Dialogue-"](value= "Silver: " + str(Silver)+  "/- " +str(Copper) + "c " )
            except BaseException:
                logging.exception("*oh no, an error D:*") 

        if event == "Clear":
            window["-G-"](value="G")
            window["-S-"](value="S")
            window["-C-"](value="C")
            window["-Dialogue-"]("")   
            
    else:
        logging.exception("Error")
        print(traceback.format_exc())
    


    





window.close()


#things to do
    #fix frame padding on bottom
    #finish the formatted output (gold as fraction when converting silver or copper)