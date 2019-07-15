#!/usr/bin/python

import bs4 as bs
from urllib.request import urlopen
import logging
import requests
import sys
import os
#from clint.textui import progress
import getopt
from tqdm import trange, tqdm
import math
import threading
from multiprocessing import Pool, freeze_support, RLock,Process

  
def download(outfname,zipurl,threadNumber):
    #mbyte = 1024*1024
    r = requests.get(zipurl, stream=True)
    if( r.status_code == requests.codes.ok ) :
        fsize = int(r.headers['content-length'])
        #logging.info("Downloading {0} tamanho: {1} MB".format(outfname,math.ceil(fsize/mbyte)))     
        try:  
            #r.iter_content(chunk_size=1024):
            with open(outfname, 'wb') as fd:            
                for chunk in tqdm(r.iter_content(1024),ascii=True, unit_divisor=1024, total=math.ceil(fsize/1024) , unit='KB', unit_scale=True,desc=outfname,position=threadNumber):
                    if chunk: # ignore keep-alive requests
                        fd.write(chunk)                                       
                fd.close()
                #logging.info("Download Conlcuido {0}".format(outfname)) 
        except Exception as e:
            print("Erro:{0}".format(e))
            #logging.error(str(e))  
    else:
        print("Falha na requisição do arquivo{0} {1}".format(outfname,r.status_code))
    #logging.info("{0} concluído".format(outfname))  
    #print("Concluído")          

def show_help():
    print("- Parametros opcionais: ")
    print("-d diretório onde serão salvos os arquivos, padrão é {0}".format(outpath))
    print("-t Quantidade de thread que será executada para fazer download simultaneamente, padrão é {0}".format(maxThreads))
        
if __name__ == "__main__":
    freeze_support() # para windows
    argv = sys.argv[1:]
    maxThreads = 1
    curdir = os.path.curdir
    outpath =  "{0}".format(os.path.join(curdir,"dados"))
    logging.basicConfig(filename='Download.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
    logging.info('Início da operação')
    url = "http://receita.economia.gov.br/orientacao/tributaria/cadastros/cadastro-nacional-de-pessoas-juridicas-cnpj/dados-publicos-cnpj/"
    
    try:
        opts, args = getopt.getopt(argv,"hi:d:t:",["help,dir,thread"])
        for opt, arg in opts:
            arg = arg.strip()
            if opt in ('-h', '--help'):
                show_help()
                sys.exit(2)

            if opt in ('-d', '--dir'):                  
                outpath = arg  
            if opt in ('-t', '--thread'):
                maxThreads = int(arg) 

    except getopt.GetoptError:
        show_help()
        sys.exit(2) 

    website = urlopen(url)
    logging.info("URL Aberta com sucesso")    
    html = website.read().decode('ISO-8859-1')
    soup = bs.BeautifulSoup(html,'lxml')       
    files = soup.find_all('a', href=True)
    try:
        path = "{0}".format(outpath)
        if not os.path.exists(path):
            os.mkdir(path)
    except:
        print("Erro ao criar diretório {0}".format(path))
        logging.error("Não foi possível criar o diretório {0}".format(path)) 
        sys.exit(2)

    threadNum = 0
    listArgs = []    
    for file in files:
        zipurl = file['href']
        
        if( zipurl.endswith('.zip') ):
            filename =zipurl.split('/')[-1]
            outfname = os.path.join(outpath,filename)                    
            args = [outfname,zipurl,threadNum]

            if maxThreads == 1:
                p = Process(target=download,args=[outfname,zipurl,threadNum])
                p.start()
                p.join()
                #download(outfname,zipurl,threadNum)
                continue

            threadNum+=1
            listArgs.append(args)
            
            
    if maxThreads > threadNum+1:
        maxThreads = threadNum+1  
    
    if maxThreads > 1 :
        p = Pool(maxThreads,initializer=tqdm.set_lock,maxtasksperchild=1,initargs=(RLock(),)) #para funcionar no windows    
        p.starmap(download,listArgs)
        p.close()
        p.join()     
        #print('\n' "Fim de processamento")
        #main(sys.argv[1:])            
