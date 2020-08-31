import requests
import re


def crawl_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    web = requests.get(url, headers=headers)
    return web.text


def BOND():
    # 美債
    usBond = crawl_page("https://finance.yahoo.com/bonds?.tsrc=fin-srch")
    pattern_usbond = re.compile(
        'class="data-col1.*?>(.*?)</td><t.*?>(.*?)</td>')
    usbond = re.findall(pattern_usbond, usBond)

    # 德債
    germanBond = crawl_page(
        "https://www.investing.com/rates-bonds/germany-10-year-bond-yield")
    pattern_germanbond = re.compile(
        'class="arial_22">(.*?)</span>\s+<s.*?>(.*?)</span>')
    germanBond = re.findall(pattern_germanbond, germanBond)

    bond_lst = [usbond[1], usbond[2], germanBond[0]]
    return bond_lst


def FOREX():
    # 從財經m平方爬取匯率資料
    Forex = []
    pattern_forex_item = re.compile(
        '<div class="stat-name">\s+<a.*?>\s+(.*?)\s+<\/a>')
    pattern_forex_num = re.compile(
        '<div class="stat-val.*?>\s+(.*?)\s+<\/div>')
    pattern_forex_delta = re.compile(
        '<span class="val-delta">\s+(.*?)\s+<\/span>')
    web = crawl_page('https://www.macromicro.me/forex')
    Forex_item = re.findall(pattern_forex_item, web)
    Forex_num = re.findall(pattern_forex_num, web)
    Forex_delta = re.findall(pattern_forex_delta, web)
    Forex.append(Forex_item)
    Forex.append(Forex_num)
    Forex.append(Forex_delta)
    Forex_lst = list(zip(Forex[0], Forex[1], Forex[2]))
    foreign_lst = [Forex_lst[0], Forex_lst[1], Forex_lst[9]]
    return foreign_lst


def RAW():
    # 從財經m平方爬取原物料資料
    Raw = []
    pattern_Raw_item = re.compile(
        '<div class="stat-name">\s+<a.*?>\s+(.*?)\s+<\/a>')
    pattern_Raw_num = re.compile('<div class="stat-val.*?>\s+(.*?)\s+<\/div>')
    pattern_Raw_delta = re.compile(
        '<span class="val-delta">\s+(.*?)\s+<\/span>')
    web = crawl_page('https://www.macromicro.me/raw-materials')
    Raw_item = re.findall(pattern_Raw_item, web)
    Raw_num = re.findall(pattern_Raw_num, web)
    Raw_delta = re.findall(pattern_Raw_delta, web)
    Raw.append(Raw_item)
    Raw.append(Raw_num)
    Raw.append(Raw_delta)
    Raw_lst = list(zip(Raw[0], Raw[1], Raw[2]))
    raw_lst = [Raw_lst[1], Raw_lst[5], Raw_lst[9], Raw_lst[13]]
    return raw_lst


def GDPandPMI():
    # 從財經m平方爬取美國、台灣gdp、pmi資料
    pattern_usaGDP = re.compile(
        'class="stat-name">(.*?)<\/div><d.*?>(.*?)<\/div>\s+<d.*?><s.*?>(.*?)<\/span>')
    web = crawl_page(
        'https://www.macromicro.me/collections/2/us-gdp-relative/12/real-gdp-growth')
    usaGDP = re.findall(pattern_usaGDP, web)

    pattern_usaPMI = re.compile(
        'class="stat-name".*?>(.*?)<\/div>\s+<d.*?>(.*?)<\/div>\s+<d.*?>\s+<s.*?>(.*?)<\/span>')
    web = crawl_page('https://www.macromicro.me/charts/7/ism')
    usaPMI = re.findall(pattern_usaPMI, web)

    pattern_twGDP = re.compile(
        'class="stat-name">(.*?)<\/div><d.*?>(.*?)<\/div>\s+<d.*?><s.*?>(.*?)<\/span>')
    web = crawl_page(
        'https://www.macromicro.me/collections/11/tw-gdp-relative')
    twGDP = re.findall(pattern_twGDP, web)

    pattern_twPMI = re.compile(
        'class="stat-name".*?>(.*?)<\/div>\s+<d.*?>(.*?)<\/div>\s+<d.*?>\s+<s.*?>(.*?)<\/span>')
    web = crawl_page(
        'https://www.macromicro.me/charts/1090/tai-wan-PMI-zhi-zao-ye-zhi-shu-ji-fei-zhi-zao-ye-zhi-shu')
    twPMI = re.findall(pattern_twPMI, web)

    gdp_lst = [usaGDP[1], twGDP[0]]
    pmi_lst = [usaPMI[0], usaPMI[1], twPMI[0], twPMI[1]]
    return gdp_lst, pmi_lst


def companyBOND():
    # 從財經m平方爬取bbb、ccc公司債資料
    pattern_bbbRate = re.compile(
        'class="stat-name".*?>(.*?)<\/div>\s+<d.*?>(.*?)<\/div>\s+<d.*?>\s+<s.*?>(.*?)<\/span>')
    web = crawl_page(
        'https://www.macromicro.me/charts/14165/us-corporate-bbb-effective-yield')
    bbbRate = re.findall(pattern_bbbRate, web)

    pattern_cccRate = re.compile(
        'class="stat-name".*?>(.*?)<\/div>\s+<d.*?>(.*?)<\/div>\s+<d.*?>\s+<s.*?>(.*?)<\/span>')
    web = crawl_page(
        'https://www.macromicro.me/charts/14169/us-corporate-ccc-or-below-effective-yield')
    cccRate = re.findall(pattern_cccRate, web)
    rate_lst = [bbbRate[0], cccRate[0]]
    return rate_lst


def TWFUTURE():
    # 從期交所上爬取期貨相關資料
    pattern_contracts = re.compile('外資<\/div>\s+<\/TD>\s+<TD.*?>\s+<d.*?>\s+<f.*?>\s+.*?<\/font>\s+<\/div>\s+<d.*?><\/div>\s+<\/TD>\s+<T.*?><d.*?>\s+.*?<\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?>\s+<d.*?><f.*?>\s+.*?<\/font><\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?>.*?<\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?><f.*?>\s+.*?<\/font><\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?>\s+.*?<\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?><f.*?>\s+(.*?)<\/font><\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?>\s+(.*?)<\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?><f.*?>\s+(.*?)<\/font><\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?>\s+(.*?)<\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?><f.*?>\s+(.*?)<\/font><\/div>\s+<d.*?><\/div><\/TD>\s+<T.*?><d.*?>\s+(.*?)<\/div>')
    web = crawl_page('https://www.taifex.com.tw/cht/3/futContractsDate')
    contracts = re.findall(pattern_contracts, web)

    pattern_putcall = re.compile('class="table_a">\s+<tr>\s+<t.*?>.*?<\/th>\s+<t.*?>.*?<\/th>\s+<t.*?>.*?<\/th>\s+<t.*?>.*?<\/th>\s+<t.*?>.*?<\/th>\s+<t.*?>.*?<\/th>\s+<t.*?>.*?<\/th>\s+<\/tr>\s+<tr>\s+<t.*?>(.*?)<\/td>\s+<t.*?>(.*?)<\/td>\s+<t.*?>(.*?)<\/td>\s+<t.*?>(.*?)<\/td>\s+<t.*?>\s+(.*?)<\/td>\s+<t.*?>\s+(.*?)<\/td>\s+<t.*?>(.*?)<\/td>')
    web = crawl_page('https://www.taifex.com.tw/cht/3/pcRatio')
    putcall = re.findall(pattern_putcall, web)
    contracts_lst = [contracts[0], contracts[3]]
    return putcall, contracts_lst


def TWelectronic():
    # 從台灣電子工業網站上爬取進出口額資料
    pattern_elec = re.compile(
        '<\/span><\/td>\s+<t.*?><s.*?>(.*?)<\/span><\/td>\s+<t.*?><s.*?>(.*?)<\/span><\/td>\s+<t.*?><s.*?>(.*?)<\/span><\/td>')
    web = crawl_page('http://www.teema.org.tw/industrial-performance.aspx')
    elec = re.findall(pattern_elec, web)

    electrionic_lst = [elec[0], elec[5], elec[6],
                       elec[11], elec[12], elec[17], elec[18], elec[23]]
    return electrionic_lst


def VIX():
    # 從investing.com上爬取sp500 vix相關資料
    pattern_index = re.compile(
        '<\/td><t.*?><a.*?>(.*?)<\/a><\/td><t.*?>(.*?)<\/td><t.*?>.*?<\/td><t.*?>(.*?)<\/td>')
    web = crawl_page('https://www.investing.com/indices/us-spx-500-futures')
    indexUSA = re.findall(pattern_index, web)
    indexUSA_lst = [indexUSA[3], indexUSA[0], indexUSA[5]]

    # 從histock及期交所上爬取台指期 vix相關資料
    pattern_twvix = re.compile('>(.*?)<\/a>\s+<\/td><t.*?>(.*?)<\/td>')
    web = crawl_page('https://info512.taifex.com.tw/Future/VIXQuote_Norl.aspx')
    twvix = re.findall(pattern_twvix, web)

    pattern_twfuture = re.compile('<h.*?>\s+(.*?)<\/h3>\s+<s.*?>.*?<\/span>\s+<s.*?><\/span>\s+<i.*? \/><a.*?>.*?<\/a>\s+<\/div>\s+<div>\s+<u.*?>\s+<li class="deal"><b>.*?<\/b><br \/>\s+<s.*?>\s+<s.*?><s.*?>(.*?)<\/span><\/span><\/span><\/li>\s+<l.*?><b>.*?<\/b><br \/>\s+<s.*?>\s+<s.*?><s.*?>.*?<\/span><\/span><\/span><\/li>\s+<l.*?><b>.*?<\/b><br \/>\s+<s.*?>\s+<s.*?><s.*?>(.*?)<\/span>')
    web = crawl_page('https://histock.tw/index-tw/FITX')
    twfuture = re.findall(pattern_twfuture, web)

    pattern_twindex = re.compile('<h.*?>\s+(.*?)<\/h3>\s+<s.*?>.*?<\/span>\s+<s.*?>.*?<\/span>\s+<\/div>\s+<\/div>\s+<d.*?>\s+<div>\s+<u.*?>\s+<l.*?><b>.*?<\/b><br \/>\s+<s.*?>\s+<s.*?>(.*?)<\/span><\/span><\/li>\s+<l.*?><b>.*?<\/b><br \/>\s+<s.*?>\s+<s.*?>.*?<\/span><\/span><\/li>\s+<l.*?><b>.*?<\/b><br \/>\s+<s.*?>\s+<s.*?>(.*?)<\/span>')
    web = crawl_page('https://histock.tw/tw')
    twindex = re.findall(pattern_twindex, web)

    indexTW_lst = [twindex[0], twfuture[0], twvix[0]]
    return indexUSA_lst, indexTW_lst
