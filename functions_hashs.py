from eth_log.models.contract import Contract
from web3 import Web3
from web3.auto import w3
import eth_event
import json
from hexbytes import HexBytes
from ast import literal_eval
from attributedict.collections import AttributeDict
def get_vars(x):
    y = str(x)
    v_1,v_2 = [],[]
    if ':' in y:
        n = str(x)[1:-1].split(',')
        for i in range(0,len(n)):
            v = str(n[i]).replace('"','').replace("'",'').replace(' ','').split(':')
            v_1.append(v[0])
            v_2.append(v[1])
    return v_1,v_2
def get_c(i):
    c = ''
    if i != 0:
        c = ','
    return c
def js_qu(x):
    if type(x) is not list:
        return '"'+str(x)+'"'
    ls = []
    for i in range(0,len(x)):
        ls.append('"'+str(x[i])+'"')
    return x
def js_qu(x):
    if type(x) is not list:
        return '"'+str(x)+'"'
    ls = []
    for i in range(0,len(x)):
        ls.append('"'+str(x[i])+'"')
    return x
def js_it(x):
    return json.loads(str(x).replace("'",'"'))
def join_it(x,y):
    return str(x)+str(y)
def get_list(x,y):
    x = t_f_js_check(x)
    for i in range(0,len(y)):
        x = str(x)[:-1] + get_c(i)+ str(y[i])+str(x)[-1]
    return x
def gen_index(y):
    n = ['indexed', 'internalType', 'name', 'type']
    z = y['type'] + ' '+y['name']
    if z not in all_vars:
        if y['name'] == '':
            if y['type'] not in types:
                types.append(z.replace(' ',''))
        else:
            if z not in all_vars:
                all_vars.append(z)
    if 'indexed' in y:
        if y['indexed'] == 'False':
            if z not in non_varis:
                non_varis.append(z)
        else:
            z = y['type'] + ' indexed '+y['name']
            if z not in ind_varis:
                ind_varis.append(z)
    return z
def get_fun(x,y,z):
    na = ['inputs','outputs']
    n = x[y]
    fun = str(y)+'()'
    kek = ''
    for i in range(0,len(na)):
        i_o = na[i]
        if i_o in n:
            nn = n[i_o]
            if str(nn) != '[]':
            
                
                fun = get_list(fun,nn)
        if i == 0:
            fun = fun + ' '+z +' returns ()'
        if i == 1:
            fun = fun
    fun = 'function '+fun+'{};'

    return str(fun).replace(' )',')')
def get_event(x,y):
    na = ['inputs','outputs']
    fun = 'event '+str(y)+'()'
    v =[]
    for i in range(0,len(na)):
        i_o = na[i]
        if i_o in n:
            for ii in range(0,len(x[i_o])):
                v.append(gen_index(js_it(t_f_js_check(x[i_o][ii]))))
            fun = get_list(fun,v)
            
    return str(fun).replace(')',');')
def get_map(x,y):
    na = ["function","fallback"]
    z = ''
    inputs = []
    out = []
    for i in range(0,len(x['inputs'])):
        inputs.append(x['inputs'][i]['type'])
    for i in range(0,len(x['outputs'])):
        out.append(x['outputs'][i]['type'])
    if len(inputs) == 2 and len(out) == 1:
        z = 'mapping ('+str(inputs[0])+' => mapping ('+str(inputs[1])+' => '+str(out[0])+')) ' +str(y)
    elif len(inputs) == 1 and len(out) == 1:
        z = 'mapping ('+str(inputs[0])+' => '+str(out[0])+') '+str(y)
    return z+';'
def t_f_js_check(x):
    y = str(x)
    tf = ['True','False'] 
    sides = [' ','"',"'"]
    for i in range(0,len(tf)):
        n_tf = tf[i]
        if n_tf in str(y):
            for ii in range(0,len(sides)):
                va = [n_tf+sides[ii],sides[ii]+n_tf]
                for iii in range(0,2):
                    v = va[iii]
                    while str(v) in str(y):
                        y = str(y).replace(v,n_tf)
            y = js_it(str(y).replace(n_tf,js_qu(n_tf)))
    return y
def splitter(x,y):
    return str(x).split(y)
def replacer(x,y):
    return str(x).replace(y,'')
def func_break(r):
    new = []
    for i in range(0,len(r)):
        x = r[i]
        x = replacer(x,'function ')
        x = splitter(x,')')[0]
        x = str(x).replace('"','').replace('(','(').replace(')',')')
 
        x = str(x).replace(x.split(' ')[0],'')
        x = x.split('(')
        name = x[0]
        varis = x[1]
        varis = varis.split(',')
        n = ''
        for ii in range(0,len(varis)):
            n = n + get_c(ii)+varis[ii].replace(varis[ii].split(' ')[-1],'')
            if ii == len(varis):
                new.append(str(name)+'('+str(n)+')')
def func_sep(x):
    x = str(x).replace(';)','","').replace('{,','{"').replace(';}','}')
    x = js_it(x)
    n = ''
    kk = []
    for i in range(0,len(x)):
        ne = str(x[i])
        name = str(splitter(str(ne).split('(')[0],' ')[-1])
        ne = str(splitter(ne,')')[0])
        ne = splitter(ne,'(')[1]
        ne = splitter(ne,',')
        n = ''
        for i in range(0,len(ne)):
            w = ne[i]
            w_1 = splitter(w,' ')
            n = n + get_c(i)+str(w).replace(str(w_1[-1]),'').replace(' indexed','')
        kk.append(str(str(name)+'('+str(n)+')').replace(' ,',',').replace(' )',')'))

    return kk
def islist(x):
    if type(x) is not list:
        return False
    return True
def disp_it(x):
    new = ''
    x = js_it(x)
    for ii in range(0,len(x)):
        n = x[ii]
        new =new+'\n'+ n
    return new
def pen(paper, place):
    with open(place, 'w') as f:
        f.write(str(paper))
        f.close()
        return
def json_up(x):
    '"'+str(x)+'"'
def kek(x):
    st = '"'+str(x)+'"'
    return w3.keccak(text=str(x)).hex()
def js_var_t(x,y):
    try:
        z = x[y]
        return True
    except:
        return False
def pub(x,y):
    if js_var_t(x,y) == True:
        if x[y] == "false":
            return 'public'
def skel_fun():
    x["name"]+'('+abi_var_parse(x,"inputs")+')'
def fun_put(x):
    x["type"]+' '+x["name"]+'('+abi_var_parse(x,"inputs")+')'+x["anonymous"]
def abi_in_out(x,y):
    na = ["type","indexed","name"]
    if js_var_t(x,y) == True:
        n = x[y]
        for i in range(0,len(n)):
            l = n[i]
            for ii in range(0,len(na)):
                m = l[na[ii]]
                if str(m) == 'true':
                    m = na[ii]
                z = z + get_c(ii)+str(m)
    return k
def abi_var_parse(x,y):
    k = []
    for i in range(0,len(y)):
        if js_var_t(x,y[i]) == True:
            k.append(x[y[i]])
    return k
        
        
        
abi = '[{"inputs":[{"internalType":"address","name":"_logic","type":"address"},{"internalType":"address","name":"admin_","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"admin_","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"implementation_","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
abi = json.loads(abi)
global kek_funs,fun_calls,ind_varis,non_varis,funs,event,const,maps,all_vars
kek_funs,fun_calls,ind_varis,non_varis,funs,event,const,maps,all_vars,types = [],[],[],[],[],[],[],[],[],[]
varis = js_it('{"all":[],"types":[],"indexed":[],"non_indexed":[]}')
ch = [],[[],[]],[]
na = ["type","name","anonymous"]
fun_calls,
for i in range(0,len(abi)):
    n = abi[i]
    for ii in range(0,len(na)):
        ch[ii].append(abi_var_parse(n,na[ii]))
    print(ch)
def reader(file):
    with open(file, 'r') as f:
        text = f.read()
        return text
def mains(x):
    from web3 import Web3
    global net,ch_id,main,file,w3,last_api,c_k,hashs_js,expo,dec
    hashs_js = ''
    last_api = [0,0]
    scan = ['avax','polygon','ethereum','cronos_test','optimism','binance']
    main = {
        'avax':{'net':'https://api.avax.network/ext/bc/C/rpc','chain':'43114','main':'AVAX'},
            'polygon':{'net':'https://polygon-rpc.com/','chain':'137','main':'MATIC'},
            'ethereum':{'net':'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161','chain':'1','main':'ETH'},
            'cronos_test':{'net':'https://cronos-testnet-3.crypto.org:8545/','chain':'338','main':'TCRO'},
            'optimism':{'net':'https://kovan.optimism.io','chain':'69','main':'OPT'},
            'binance':{'net':'https://bsc-dataseed.binance.org/','chain':'56','main':'bsc'}
            }
    expo = ''
    dec = ''
    main = main[x]
    net,ch_id,main,file,w3 = main['net'],main['chain'],main['main'],str(x)+'.txt',Web3(Web3.HTTPProvider(main['net']))
    c_k = 0
    return net,ch_id,main,file,w3
for i in range(0,len(abi)):
    n = abi[i]
    na = ['inputs','outputs']
    ls = js_it('{}')
    name,typ = '',''
    maping = 0
    ll = ''
    if 'name' in n:
        name = n['name']
        fun_calls.append(name)
    if 'stateMutability' in n:
        mute = n['stateMutability']
    if 'type' in n:
        typ = n['type']
    if 'inputs' in n:
        if str(n['inputs']) != '[]':
            #print(n['inputs'])
            if n['inputs'][0]['name'] == '':
                maping = 1
    #print(name,typ)
    ls = js_it(str(ls)[:-1] + get_c(len(ls)) + str(js_qu(name)+':{}')+str(ls)[-1])
    if int(maping) == int(0) and typ == 'function':
        for ii in range(0,len(na)):
            n_na = na[ii]
            ns = join_it(js_qu(n_na),':[]')
            ls[name] = js_it(str(ls[name])[:-1] + get_c(len(ls[name])) + str(ns)+str(ls[name])[-1])
            for iii in range(0,len(n[n_na])):
                ls[name][n_na].append(gen_index(n[n_na][iii]))
            if str(n_na) in str(n) and str(n[n_na]) != '[]':
                n_y = t_f_js_check(n[n_na][0])
                y = js_it(n_y)
        #kek_funs.append(str(name)+'('+str(ls).replace("'",'').replace('[','').replace(']','')+')')
        funs.append(get_fun(ls,name,mute))
    elif typ == 'constructor':
        const.append(str(typ)+'(){};')
    elif typ == 'event':
        event.append(get_event(n,name))
    elif int(maping) == int(1) and typ == 'function':
        maps.append(get_map(n,name))
    #nmm = input(str(abi[i])+'\n '+str(funs))
mains('binance')
varis['types'] = types
varis['all'] = all_vars
varis['indexed'] = ind_varis
varis["non_indexed"]=non_varis
new_all = ''
#print(kek_funs)
x = [event,maps,const,funs]
new = ''
for i in range(0,len(x)):
    new = new + ',\n'+str(disp_it(x[i])).replace("'",'"')
pen('{'+str(new).replace('\n','').replace(';,',';').replace(';;',';').replace("'",'"')+'}','funcs.json')

pen([event,maps,funs],'funcs.json')
r = js_it(str([event,funs,event]))
k = []
for i in range(0,len(r)):
    k.append(func_sep(r[i]))
k = js_it(str(k).replace('], [',',')[1:-1].replace('nt128,','int128,').replace('iint128','int128'))

d = []
nam = []
for i in range(0,len(k)):
    ll = k[i].replace(')','),')
    l = k[i].split('(')[0]
    nam.append(l)
    d.append(k[i].replace(') ',')'))
v = []
n_nam = []
for i in range(0,len(k)):
    v.append(kek(k[i]))
    if nam[i] not in n_nam:
        n_nam.append(nam[i])
        print('uint256 public _'+str(nam[i])+'_ = ',v[i],';')
print(d,v)
pen(str(d)+','+str(v),'dv_funs.txt')
