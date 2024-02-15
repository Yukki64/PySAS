import sys
sys.dont_write_bytecode = True #t1 No bytecode



def cardinal(): #t2 main.
    import argparse
    from PIL import Image
    import json
    from os import listdir, mkdir
    
    parser = argparse.ArgumentParser(
        prog = f"{__file__.split(chr(47))[-1].split(chr(92))[-1].rsplit(chr(46), 1)[0]}", # This returns the file name
        description = "Slices a sprite atlas to separate all of it's sprites into individual images in a folder.",
        epilog = "This is not a graphical application! You must indicate a file at minimum!"
        )
    
    parser.add_argument("spriteAtlas", help="any valid sprite atlas image file.")
    parser.add_argument("-j", "--json", help="indicate where sprite atlas JSON file is located.")
    parser.add_argument("-o", "--output", help="the folder location at which sliced sprites will be output to.")
    parser.add_argument("-s", "--silent", action="store_true", help="disable terminal output, don't prompt when action is needed.")
    parser.add_argument("-v", "--verbose", action="store_true", help="print execution in terminal.")
    
    args = parser.parse_args()
    
    spriteAtlasLoc = args.spriteAtlas
    jsonLoc = args.json
    outputLoc = args.output
    silentExec = args.silent
    verbosity = args.verbose
    
    osSlash = spriteAtlasLoc[max(spriteAtlasLoc.rfind("/"), spriteAtlasLoc.rfind("\\"))] # Returns which of forward/back slash the OS uses
    
    if verbosity:
        print(f"\nArguments: [spriteAtlasLoc: {spriteAtlasLoc}], [jsonLoc: {jsonLoc}], [outputLoc: {outputLoc}], [silent: {silentExec}], [verbosity: {verbosity}].")

    try: # checks if a valid image is given
        atlasImg = Image.open(spriteAtlasLoc)
        if verbosity:
            print(f"\nValid sprite atlas image found: [format: {atlasImg.format}].")
    except IOError:
        raise IOError
    
    if jsonLoc == None: # If no json is provided, sets json to path\spriteAtlas.json
        jsonLoc = f"{spriteAtlasLoc.rsplit(chr(46), 1)[0]}.json"
        if verbosity:
            print(f"\nNo file json file specified. Parameter modified: [location: {jsonLoc}].")

    try: # checks if valid json is given
        jsonFile = open(jsonLoc)
        jsonData = json.load(jsonFile)
        if verbosity:
            print(f"\nValid JSON found: [location: {jsonLoc}]")
    except IOError:
        raise IOError

    if outputLoc == None: # If no path provided, sets path to path\spriteAtlas
        outputLoc = spriteAtlasLoc.rsplit(chr(46), 1)[0]
        if verbosity:
            print(f"\nNo output folder specified. Parameter modified: [location: {outputLoc}].")
        
    try:
        if verbosity:
            print("\nLooking if output directory exists...")   
        if listdir(outputLoc):
            if verbosity:
                print("\nOutput directory exists but is not empty!")
                
            if silentExec:
                userInput = "yes"
            else:
                userInput = input("\nOutput directory already exists with files inside of it. Proceed anyways? (y/N) : ").lower()
                
            if not userInput in ["yes", "ye", "y"]:
                print("\nOperation canceled.")
                exit()
            else:
                if not silentExec or verbosity:
                    print("\nUser prompt accepted. Proceeding...")
        else:
            if verbosity:
                print("\nOutput directory exsists and is empty! Proceeding...")
    except IOError: # IOError required to keep this from executing after try???
        if not silentExec or verbosity:
            print("\nOutput directory does not exist! Creating...")
        mkdir(outputLoc)
    
    if not silentExec or verbosity:
        print("\nSlicing sprite atlas...\n")
    
    for idx, i in enumerate(jsonData["frames"]): # Slices each sprites from the sprite atlas and outputs them.
        if not silentExec or verbosity:
            print(f'\033[K[Current sprite from atlas: "{i}" ({idx + 1} / {len(jsonData["frames"])})] ({round(100 * float(idx + 1)/float(len(jsonData["frames"])))}%) ', end="\r")
        cropX = jsonData["frames"][i]["frame"]["x"]
        cropY = jsonData["frames"][i]["frame"]["y"]
        cropW = jsonData["frames"][i]["frame"]["w"]
        cropH = jsonData["frames"][i]["frame"]["h"]
        cropBox = (cropX, cropY, cropX + cropW, cropY + cropH)
        atlasImg.crop(cropBox).save(f"{outputLoc}{osSlash}{i.rsplit(chr(46), 1)[0]}.{atlasImg.format}", atlasImg.format)
    
    if not silentExec or verbosity:
        print(f'\n\nDone! See the "{outputLoc}" folder.')



if __name__ == "__main__": #t3 Doesn't run on import
    cardinal()
else: #t4 Runs on import
    print(f'"{__file__.split(chr(47))[-1].split(chr(92))[-1].rsplit(chr(46), 1)[0]}" is not meant to be imported. You may remove it from your script.')



# Original script available at: https://github.com/Yukki64/PySAS