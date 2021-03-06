#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re,xbmc
import unicodedata,htmlentitydefs

#Je garde le nom kepliz pour pas perturber
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz'
SITE_DESC = 'Films en streaming'
#URL_HOST = 'http://www.grudal.com/'
URL_HOST = 'http://www.ozporo.com/'
URL_MAIN = 'URL_MAIN'
FILMPATTERN = '<div class="article-content"><p style="text-align: center;"><img src="(.+?)" border.+?<p style="text-align: left;">([^<>]+?)<\/p>'
SEARCHPATTERN = '<fieldset> *<div> *<b><a *href="\/[0-9a-zA-Z]+\/(.+?)" *>(.+?)<\/a><\/b>'
NORMALPATTERN = '<span style="list-style-type:none;" >.+? href="\/[0-9a-zA-Z]+\/(.+?)">(.+?)<\/a>'
NEXTPAGEPATTERN = '<span class="pagenav">[0-9]+<.span><.li><li><a title=".+?" href="\/[0-9a-zA-Z]+\/(.+?)" class="pagenav">'
FRAMEPATTERN = 'GRUDALpluginsphp\("player1",{link:"(.+?)"}\);'
FRAMEPATTERN2 = '<iframe src= *(?:"|)([^<>"]+\/player\.php\?id=.+?)"' #'<iframe src="*\/([^<>"]+\/player\.php\?id=.+?)"'
HOSTPATTERN = '"link":"([^"]+?)","label":"([^"]+?)"'

#pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_HD = (URL_MAIN, 'showMovies')

ANIM_NEWS = (URL_MAIN + 'index.php?option=com_content&view=category&id=2&Itemid=2', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'index.php?option=com_content&view=category&id=2&Itemid=2', 'showMovies')
DOC_NEWS = (URL_MAIN + 'index.php?option=com_content&view=category&id=26', 'showMovies')
DOC_DOCS = ('http://', 'load')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'index.php?option=com_content&view=category&id=3')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Spectacles', 'doc.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['A l\'affiche',URL_MAIN + 'index.php?option=com_content&view=category&id=29'] )
    liste.append( ['Action',URL_MAIN + 'index.php?option=com_content&view=category&id=1'] )
    liste.append( ['Animation',URL_MAIN + 'index.php?option=com_content&view=category&id=2'] )
    liste.append( ['Aventure',URL_MAIN + 'index.php?option=com_content&view=category&id=4'] )
    liste.append( ['Comédie',URL_MAIN + 'index.php?option=com_content&view=category&id=6'] )
    liste.append( ['Documentaires',URL_MAIN + 'index.php?option=com_content&view=category&id=26'] )
    liste.append( ['Drame',URL_MAIN + 'index.php?option=com_content&view=category&id=7'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'index.php?option=com_content&view=category&id=9'] )
    liste.append( ['Fantastique',URL_MAIN + 'index.php?option=com_content&view=category&id=8'] )
    liste.append( ['Policier',URL_MAIN + 'index.php?option=com_content&view=category&id=10'] )
    liste.append( ['Science Fiction',URL_MAIN + 'index.php?option=com_content&view=category&id=11'] )
    liste.append( ['Spectacle',URL_MAIN + 'index.php?option=com_content&view=category&id=3'] )
    liste.append( ['Thriller',URL_MAIN + 'index.php?option=com_content&view=category&id=12'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showMovies(sSearch = ''):
    oGui = cGui()
 
    if sSearch :
        #limite de caratere sinon bug de la recherche
        sSearch = sSearch[:20]
        sUrl = URL_MAIN + 'index.php?ordering=&searchphrase=all&Itemid=1&option=com_search&searchword=' + sSearch
        sPattern = SEARCHPATTERN
    else :
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = NORMALPATTERN

    oParser = cParser() 
        
    #L'url change tres souvent donc faut la retrouver
    req = urllib2.Request(URL_HOST)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    sMainUrl = ''
    aResult = oParser.parse(data, 'window\.location\.href="([0-9a-zA-Z]+)";')
    if aResult[0]:
        #memorisation pour la suite
        sMainUrl = URL_HOST + aResult[1][0] + '/'
        #correction de l'url
        sUrl = sUrl.replace('URL_MAIN', sMainUrl )
    else:
        #Si ca marche pas, pas la peine de continuer
        return
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sTitle2 = aEntry[1]
            sTitle2 = re.sub('<font color="#[0-9]{6}" *><i>HD<\/i><\/font>', '[HD]',sTitle2)
            sUrl2 = aEntry[0]
           
            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            
            sDisplayTitle = cUtil().DecoTitle(sTitle2)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sMainUrl + str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle2))
            oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sMainUrl + sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sHtmlContent):
    sPattern = NEXTPAGEPATTERN
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
   
    sThumb = ''
    sComm = ''
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    
    #Recuperation info film, com et image
    sPattern = FILMPATTERN
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sThumb = aResult[1][0][0]
        sComm = cUtil().unescape(aResult[1][0][1])
 
    #Recuperation info lien du stream.
    sLink = None
    sPostUrl = None
    sHtmlContent = sHtmlContent.replace('\r','')
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    #Format classique
    sPattern = FRAMEPATTERN
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sLink = aResult[1][0]
        sPattern = '\/plugins\/([0-9a-zA-Z]+)\/plugins\/GRUDALpluginsphp.js"><\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sPostUrl = sMainUrl + 'plugins/' + aResult[1][0] + '/plugins/GRUDALpluginsphp.php'
            
        if ((sLink) and (sPostUrl)):

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sLink', sLink)
            oOutputParameterHandler.addParameter('sPostUrl', sPostUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', sDisplayTitle, sThumb, sThumb, sComm, oOutputParameterHandler)
            
    #Format rare
    if not sLink:
        sPattern = FRAMEPATTERN2
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sLink = aResult[1][0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sLink', sLink)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink2', sDisplayTitle, sThumb, sThumb, sComm, oOutputParameterHandler)

    oGui.setEndOfDirectory()
   
def showHostersLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sLink = oInputParameterHandler.getValue('sLink')
    sPostUrl = oInputParameterHandler.getValue('sPostUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
    headers = {'User-Agent': UA ,
               'Host' : 'ozporo.com',
               'Referer': sUrl,
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding' : 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
               
    post_data = {'link' : sLink}
    
    req = urllib2.Request(sPostUrl , urllib.urlencode(post_data), headers)
    
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    
    oParser = cParser()
    sPattern = HOSTPATTERN
    aResult = oParser.parse(data, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sLink = aEntry[0]
            Squality = aEntry[1]
            sTitle = sMovieTitle.replace(' [HD]','')
            sTitle = '[' + Squality + '] ' + sTitle
           
            sHosterUrl = str(sLink)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
           
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
            cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()

def showHostersLink2():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sLink = oInputParameterHandler.getValue('sLink')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    headers = {'User-Agent': UA ,
               'Host' : 'grudal.com',
               'Referer': sLink,
               'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
               'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               'Range' : 'bytes=0-'
               #'Accept-Encoding' : 'gzip, deflate',
               #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
               } 
               
    req = urllib2.Request(sLink)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    
    oParser = cParser()
    sPattern = '"file":"(.+?)","type":"mp4","label":"(.+?)"'
    aResult = oParser.parse(data, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sLink = aEntry[0].replace('\/','/')
            Squality = aEntry[1]
            sTitle = sMovieTitle.replace(' [HD]','')
            sTitle = '[' + Squality + '] ' + sTitle
            
            #decodage des liens          
            req = urllib2.Request(sLink,None,headers)
            try:
                response = urllib2.urlopen(req)
                #data = response.read()
                response.close()
            except urllib2.URLError, e:
                sLink = e.geturl()
            
            sHosterUrl = str(sLink)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
           
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
            cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
