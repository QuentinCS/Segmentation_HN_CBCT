from xml.dom import minidom
import fileinput
import sys

def update_mac(prim_per_proj,number_jobs):
    filename = './data/elektaGeometry.xml'
    num_projs = count_projs(filename)
    print("proj : ", num_projs)

    for line in fileinput.input("./mac/primary-patient.mac", inplace=True):
        if "/gate/application/setTimeStop" in line:
            print(f'/gate/application/setTimeStop {num_projs} ns')
        elif "/gate/application/setTotalNumberOfPrimaries" in line:
            print(f'/gate/application/setTotalNumberOfPrimaries {num_projs}')
        else:
            print(line, end='')


    filename = './data/elektaGeometry_lessprojections.xml'
    num_projs = count_projs(filename)
    for line in fileinput.input("./mac/scatter-patient.mac", inplace=True):
        if "/gate/application/setTimeStop" in line:
            print(f'/gate/application/setTimeStop {num_projs} ns')
        elif "/gate/application/setTotalNumberOfPrimaries" in line:
            print(f'/gate/application/setTotalNumberOfPrimaries {int(prim_per_proj/number_jobs)*num_projs}')
        else:
            print(line, end='')

def update_mac_V2(prim_per_proj,number_jobs, folder):
    filename = f'{folder}/data/elektaGeometry.xml'
    num_projs = count_projs(filename)
    print("proj : ", num_projs)

    for line in fileinput.input(f'{folder}/mac/primary-patient.mac', inplace=True):
        if "/gate/application/setTimeStop" in line:
            print(f'/gate/application/setTimeStop {num_projs} ns')
        elif "/gate/application/setTotalNumberOfPrimaries" in line:
            print(f'/gate/application/setTotalNumberOfPrimaries {num_projs}')
        else:
            print(line, end='')

    filename = f'{folder}/data/elektaGeometry.xml'
    num_projs = count_projs(filename)
    for line in fileinput.input(f'{folder}/mac/scatter-patient.mac', inplace=True):
        if "/gate/application/setTimeStop" in line:
            print(f'/gate/application/setTimeStop {num_projs} ns')
        elif "/gate/application/setTotalNumberOfPrimaries" in line:
            print(f'/gate/application/setTotalNumberOfPrimaries {prim_per_proj}')
            #print(f'/gate/application/setTotalNumberOfPrimaries {int(prim_per_proj/number_jobs)*num_projs}') 
        else:
            print(line, end='')

def count_projs(filename):
    # parse xml file by name
    mydoc = minidom.parse(filename)
    items = mydoc.getElementsByTagName('Projection')
    return len(items)

def del_projs(filename, output_filename, factor):
    print("ok")
    # keep 1/factor of the projections
    mydoc = minidom.parse(filename)
    items = mydoc.getElementsByTagName('Projection')

    for i, item in enumerate(items):
        if (i % factor != 0):
            parent = item.parentNode
            parent.removeChild(item) 

    with open(output_filename,"w") as fs:
        fs.write(mydoc.toxml())
        fs.close()

if __name__ == "__main__":
    prim_per_proj = int(sys.argv[1])
    number_jobs = int(sys.argv[2])
    update_mac(prim_per_proj,number_jobs)
