import csv 
import argparse
import time
import os
from multiresampler import create_directory

def make_directories(sheet, start, stop, usr):

    with open(sheet) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        
        next(readCSV) # Skip the first row which contains the header
        id = -1 # In order to make first row a new id
        counter = 0
        names = []
        for row in readCSV:
            print(row)
            if row[0] in (None, ''):
                print('Row skip!')
                continue

            
            swath_id = int(row[0].strip())

            print('ID: ' + row[0])
            if swath_id >= start and swath_id <= stop:
                heading = row[6].strip()
                if swath_id != id:
                    id = swath_id
                    print("New ID: " + str(id))

                    print("Heading number: " + heading)
                    headings = [heading]

                    dir = str(id).zfill(3) + '_' + heading
                    print(dir)
                    create_directory(dir)
                    
                
                elif swath_id == id and heading not in headings:
                    headings.append(heading)

                    new_dir = dir + '_' + heading # Adding second heading number including name
                    try:
                        os.rename(dir, new_dir)
                    except FileExistsError:
                        print("Directory " , new_dir ,  " already exists")
                    dir = new_dir
                    print("New directory name: " + dir)
            
                name = row[7].strip()
                if not name: #Not empty string
                    print("Empty String " + str(swath_id))
                elif name in names:
                    print("Error: Name already in names. swath ID: " + str(swath_id) + " Name: " + name)
                else:
                    names.append(name)
                    counter += 1
                    print("Counter: " + str(counter) + ", Swath ID: " + str(swath_id) + ", Name: " + name)

                    hewa_download(usr, dir, name)
                
                

            else:
                print('Swath ID out of bounds: ' + str(start) + ', ' + str(stop))
        print(counter)
        print(len(names))
            


def hewa_download(user, saveto, file_name):
    #
    # Download files from hewa onto local directory
    # Assumes local system has access key to @hewa
    #
    ann = file_name + ".ann"
    print("annotation file: " + ann)
    grd = file_name + ".hgt.grd"
    print("grid file: " + grd)

    start_time = time.time()
    #os.system("scp " + user + "@hewa://project/glistin/data/" + file_name + "/" + ann + " " + saveto)
    #os.system("scp " + user + "@hewa://project/glistin/data/" + file_name + "/" + grd + " " + saveto)
    
    os.system("rsync -auvz " + user + "@hewa://project/glistin/data/" + file_name + "/" + ann + " " + saveto)
    os.system("rsync -auvz " + user + "@hewa://project/glistin/data/" + file_name + "/" + grd + " " + saveto)
    
    print("Download runtime: --- %s seconds ---" % (time.time() - start_time))

    '''
    privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    ssh.connect(IP[0], username = user[0], pkey = mykey)
    '''
    
    '''
    ftp_client=ssh_client.open_sftp()
    ftp_client.get(‘remotefileth’,’localfilepath’)
    ftp_client.close()
    '''
if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    #
    # Format for adding an argument:
    # parser.add_argument("-x", "--fullname", action="store", help="comment", default=default value, dest="variable_name",  type=datatype, required=T/F)
    #
    parser.add_argument("-c", "--csv", action="store", help="Complete path to csv file to be read", dest="file", type=str, required=True)
    parser.add_argument("-s", "--save", action="store", help="Complete path to save the directories to", dest="save", type=str, required=True)
    parser.add_argument("-u", "--usr", action="store", help="Username for Hewa", dest="user", type=str, required=True)
    parser.add_argument("-i", "--startID", action="store", help="First ID to make directory for", default=1, dest="start",  type=int, required=False)
    parser.add_argument("-I", "--stopID", action="store", help="Last ID to make directory for", dest="stop", default=81, type=int, required=False)
    args = parser.parse_args()

    os.chdir(args.save) # Be sure to make directories in the desired directory
    make_directories(args.file, args.start, args.stop, args.user)
    print("Total runtime of parsedirectories: --- %s seconds ---" % (time.time() - start_time))
    print("Done!")