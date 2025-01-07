import pandas as pd
import glob
import numpy as np
import re

mcda_sizes = {
    'PSL_0.6-40':
        '0.244381	0.246646	0.248908	0.251144	0.253398	0.255593	0.257846	0.260141	0.262561	0.265062	0.267712	0.27037	0.273159	0.275904	0.278724	0.281554	0.284585	0.287661	0.290892	0.294127	0.297512	0.300813	0.304101	0.307439	0.310919	0.314493	0.318336	0.322265	0.326283	0.330307	0.334409	0.338478	0.342743	0.347102	0.351648	0.356225	0.360972	0.365856	0.371028	0.376344	0.382058	0.387995	0.394223	0.400632	0.407341	0.414345	0.42174	0.429371	0.437556	0.446036	0.454738	0.463515	0.472572	0.481728	0.491201	0.500739	0.510645	0.52072	0.530938	0.541128	0.551563	0.562058	0.572951	0.583736	0.594907	0.606101	0.617542	0.628738	0.640375	0.652197	0.664789	0.677657	0.691517	0.705944	0.721263	0.736906	0.753552	0.770735	0.789397	0.80869	0.82951	0.851216	0.874296	0.897757	0.922457	0.948074	0.975372	1.003264	1.033206	1.064365	1.09709	1.130405	1.165455	1.201346	1.239589	1.278023	1.318937	1.360743	1.403723	1.446	1.489565	1.532676	1.577436	1.621533	1.667088	1.71252	1.758571	1.802912	1.847836	1.891948	1.937088	1.981087	2.027604	2.074306	2.121821	2.168489	2.216644	2.263724	2.312591	2.361099	2.41222	2.464198	2.518098	2.571786	2.628213	2.685162	2.745035	2.80545	2.869842	2.935997	3.005175	3.074905	3.148598	3.224051	3.305016	3.387588	3.476382	3.568195	3.664863	3.761628	3.863183	3.965651	4.07283	4.17905	4.289743	4.400463	4.512449	4.621025	4.73153	4.83992	4.949855	5.057777	5.169742	5.281416	5.395039	5.506828	5.621488	5.734391	5.849553	5.962881	6.081516	6.200801	6.322133	6.441786	6.56513	6.686935	6.813017	6.938981	7.071558	7.205968	7.345185	7.483423	7.628105	7.774385	7.926945	8.0805	8.247832	8.419585	8.598929	8.780634	8.973158	9.167022	9.37276	9.582145	9.808045	10.041607	10.287848	10.537226	10.801172	11.068405	11.345135	11.621413	11.910639	12.200227	12.492929	12.780176	13.072476	13.359067	13.651163	13.937329	14.232032	14.523919	14.819204	15.106612	15.40211	15.695489	15.998035	16.297519	16.610927	16.9268	17.250511	17.570901	17.904338	18.239874	18.588605	18.938763	19.311505	19.693678	20.093464	20.498208	20.927653	21.366609	21.827923	22.297936	22.802929	23.325426	23.872344	24.428708	25.016547	25.616663	26.249815	26.888493	27.563838	28.246317	28.944507	29.626186	30.32344	31.005915	31.691752	32.3539	33.030123	33.692286	34.350532	34.984611	35.626553	36.250913	36.878655	37.489663	38.12155	38.748073	39.384594	40.00854	40.654627	41.292757	41.937789	42.578436',
    'PSL_0.15-17':
        '0.147178	0.148512	0.14984	0.151149	0.152463	0.153736	0.155037	0.156353	0.157733	0.159147	0.160631	0.162104	0.163632	0.165116	0.166619	0.168103	0.169663	0.171215	0.172809	0.174372	0.175972	0.177499	0.17899	0.180473	0.181989	0.183515	0.185125	0.18674	0.188361	0.189958	0.191562	0.193131	0.194757	0.196404	0.198108	0.199817	0.201587	0.203405	0.205329	0.207304	0.209425	0.211626	0.213932	0.216303	0.218782	0.221367	0.224093	0.226903	0.229915	0.233032	0.236228	0.23945	0.242773	0.246132	0.249607	0.253107	0.256744	0.260442	0.264187	0.267911	0.271706	0.275499	0.279403	0.283227	0.287138	0.290997	0.294872	0.29859	0.30237	0.306117	0.310001	0.313851	0.317863	0.321889	0.326007	0.330069	0.334253	0.338447	0.34288	0.347352	0.352069	0.356884	0.361907	0.366927	0.372137	0.377479	0.383123	0.38886	0.395014	0.40144	0.408224	0.415169	0.422523	0.430111	0.438266	0.446544	0.455456	0.464683	0.47431	0.483937	0.494039	0.504239	0.515062	0.525963	0.537475	0.549211	0.561363	0.573305	0.585638	0.597968	0.610797	0.623491	0.637091	0.650905	0.665095	0.679159	0.693809	0.708272	0.723433	0.738634	0.754816	0.771442	0.788866	0.806406	0.825041	0.844056	0.864269	0.884896	0.907133	0.930247	0.954702	0.979641	1.006303	1.033916	1.063887	1.094818	1.128497	1.163781	1.201442	1.239666	1.280344	1.321963	1.366094	1.410407	1.457152	1.504424	1.552681	1.599797	1.647969	1.695302	1.74325	1.790112	1.838436	1.886361	1.934874	1.982394	2.030952	2.078624	2.127138	2.174776	2.224535	2.274453	2.325111	2.374953	2.426211	2.476709	2.528855	2.580825	2.635387	2.690558	2.747551	2.803991	2.862899	2.922291	2.984056	3.046042	3.113385	3.182289	3.254006	3.326432	3.402919	3.479686	3.56089	3.643269	3.731866	3.82319	3.919206	4.01622	4.118729	4.222422	4.329813	4.437176	4.549892	4.663274	4.778641	4.892855	5.010383	5.12713	5.24763	5.367036	5.491243	5.615306	5.74164	5.86515	5.99241	6.118721	6.248725	6.377145	6.511253	6.646127	6.784049	6.920263	7.061721	7.203762	7.351069	7.498659	7.655424	7.815799	7.983194	8.152294	8.331328	8.513941	8.705466	8.90023	9.109121	9.324911	9.550495	9.779767	10.021903	10.269101	10.529969	10.793235	11.071817	11.35364	11.642367	11.92479	12.214337	12.498558	12.785157	13.062966	13.34801	13.628646	13.909346	14.181604	14.459354	14.731797	15.008272	15.280104	15.564339	15.849489	16.142262	16.431695	16.733284	17.03231	17.334961	17.635557',
    'water_0.6-40':
        '0.475328874	0.476797513	0.478175666	0.479502075	0.480855492	0.482239192	0.483776821	0.485514795	0.487586124	0.490033954	0.493015369	0.49644285	0.500526891	0.504620049	0.508623279	0.512432791	0.516276412	0.519917789	0.523446881	0.526657368	0.529644951	0.532170415	0.534453013	0.536612172	0.538707124	0.540707499	0.542704885	0.544602005	0.546412089	0.548115794	0.54976444	0.551336908	0.552945782	0.5545795	0.556307547	0.558111326	0.560094002	0.56230309	0.564890776	0.567889907	0.571592672	0.576088823	0.581680177	0.588617321	0.601561496	0.630479813	0.676961544	0.710966886	0.735991613	0.756999913	0.775663514	0.795802163	0.817335328	0.834507604	0.851033998	0.86681952	0.883636475	0.904097147	0.945168374	0.987512487	1.00945989	1.024622743	1.037300638	1.04742767	1.055919888	1.062703414	1.067781829	1.071556532	1.074791681	1.07782548	1.081217504	1.085261064	1.090688654	1.099784657	1.101313854	1.134070536	1.209881892	1.226633942	1.276581131	1.281214165	1.299169605	1.401316835	1.41500474	1.488659509	1.499543839	1.530187633	1.612875286	1.666529026	1.676728327	1.692803248	1.697021378	1.743202139	1.774124289	1.79524413	1.845877084	1.860421324	2.020064767	2.022618315	2.088301883	2.15270898	2.166822976	2.19656516	2.196871589	2.366985679	2.567716135	2.713412113	3.023724973	3.116313593	3.258662351	3.499997015	3.560935854	3.656816689	3.701894939	4.128937642	4.246310184	4.294054709	4.442235484	4.449948153	4.653026664	4.653982923	4.67225491	4.861758846	5.128331636	5.178882979	5.3989097	5.488764992	5.697755771	5.796959675	5.849201526	5.861379666	6.181802879	6.234781395	6.270167934	6.456362015	6.664095866	6.818273185	7.045264319	7.199039758	7.744351806	8.149762235	8.389541055	9.106277016	9.376108012	9.458106894	9.720177509	9.891769321	9.893218147	10.08342955	11.13544922	11.3674229	11.97956261	12.05205985	12.13275325	12.52580911	12.65504996	12.74203407	13.5130931	13.60890061	14.00643198	14.01971045	14.62845349	14.68718025	15.08350885	15.08634042	15.26579923	15.48530688	15.78181646	15.87183591	15.88837124	15.99151022	16.21562139	16.3392285	17.09296412	17.30950528	17.49875152	17.91853132	18.81127331	18.88275366	19.49931861	20.50310055	20.67596729	21.43256304	21.66692463	22.38056288	22.41687813	23.32114574	23.59800118	24.6884587	26.15910161	26.40985223	26.54907612	26.82122253	27.95378788	28.31828571	28.62308926	28.9859605	31.70831679	33.30483755	33.31872983	33.47237149	33.83613691	34.14117219	34.29535607	35.96238407	36.45040779	36.96988842	39.31445632	39.80082648	39.97625745	40.4735219	41.12239047	41.36883415	41.44721931	42.14962289	43.5535701	44.66132244	45.18348652	45.4997003	45.62804903	46.07948013	47.22685994	47.31823406	48.04153067	50.09042257	51.10002286	51.70165447	54.88557633	54.89575025	56.84483279	57.63884448	59.89426308	62.48060031	65.02975953	65.31940219	66.72726474	66.93637203	68.96794765	70.10028923	73.92440633	74.13015358	74.791476	78.61039438	81.12774565	81.78167273	84.31901307	87.67904454	87.73430049	88.07791102	88.92650157	89.09216846	89.90121531	90.14220699	93.09415699	94.34675245	95.23367622	99.56794522',
    'water_0.15-17':
        '0.19227805	0.195682843	0.198983343	0.20211289	0.205059225	0.207724906	0.210261443	0.212640197	0.214941426	0.217106159	0.219184031	0.221069702	0.222864072	0.224475983	0.226007321	0.227451721	0.228935989	0.230420372	0.232001183	0.23365707	0.235515886	0.237498239	0.2396823	0.24214974	0.245031001	0.248355538	0.252390654	0.257053516	0.262427305	0.268474128	0.275372623	0.282991081	0.29186836	0.307406033	0.399923672	0.402950618	0.406095451	0.409547965	0.413400206	0.41751259	0.422044242	0.42680368	0.431777327	0.436801452	0.441881131	0.446916295	0.451869098	0.456536345	0.461007333	0.465043657	0.468581314	0.47159057	0.474204957	0.476473849	0.478591721	0.480677994	0.48300681	0.485758086	0.489139191	0.49325646	0.498338142	0.504028299	0.509556422	0.514585055	0.519317611	0.523556277	0.527348524	0.530511705	0.533271375	0.535775297	0.538169182	0.540358784	0.542467011	0.544426232	0.546291497	0.548017646	0.549703069	0.551325101	0.552997124	0.554673551	0.55647017	0.558378723	0.56050201	0.562815814	0.565485426	0.568582588	0.572346583	0.576807678	0.58246436	0.589712032	0.604097302	0.635149648	0.681785255	0.713426518	0.737929379	0.758135266	0.777197248	0.798828865	0.820820152	0.838396525	0.855899917	0.87246732	0.89199909	0.922871585	0.974103329	1.005591361	1.023715678	1.037668183	1.049003877	1.057952428	1.064979646	1.069897601	1.073922024	1.077493706	1.081305379	1.085788096	1.091724556	1.102779697	1.143265693	1.143675182	1.163586446	1.246663736	1.281034981	1.289349324	1.374261238	1.401296895	1.415000046	1.428202899	1.456793	1.496478358	1.51027838	1.547046871	1.573966487	1.607826932	1.61288441	1.673303193	1.682765991	1.700659399	1.712959793	1.752359685	1.764561073	1.963587787	1.975472036	2.018506015	2.109050442	2.137584399	2.163430246	2.198779576	2.206574596	2.521503927	2.600807492	2.930644138	3.224767773	3.26559294	3.299391563	3.468402268	3.55387855	4.015901324	4.14533435	4.15481853	4.204793932	4.306427442	4.484413043	4.509869078	4.659718938	5.012878336	5.02631696	5.094605209	5.216818908	5.421478915	5.465600408	5.466342553	5.792080706	5.800707245	5.801478634	5.896858039	6.314835626	6.344372707	6.479563152	6.717522876	6.889473096	7.196842924	7.385283045	7.599896247	7.722296477	7.896454473	7.921113299	8.543756839	9.095455989	9.16683766	9.340296673	9.527426832	9.70141772	11.10018093	11.16424998	11.373042	12.25953607	12.46820121	12.59184634	12.89654491	12.91132697	13.34641457	13.9706481	14.15548153	14.28459638	14.42672431	14.59952971	15.21856797	15.50879655	15.60034721	15.92875268	16.35351736	16.37616054	16.42409686	16.83332527	17.12982341	17.31701994	18.02256439	18.16605357	18.20476917	18.49994924	19.20076453	19.39154934	21.89001477	21.99989778	21.99993105	23.30541595	23.58030073	23.99543799	24.04375695	25.18505013	25.56282424	26.15732199	26.34740847	26.4192903	27.51664818	27.78718441	28.68872451	30.81710534	31.19347354	32.34758429	32.53704978	33.36324834	33.46006639	33.50015573	34.33790788	34.94707083	35.5539353	35.59328655	35.70406319	35.98700435	36.75952545	37.4023428	39.35282551	39.88672896	41.79105594'}


def preprocess_bme(file):
    df = pd.read_csv(file)
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df = df.drop(['date', 'time'], axis=1)
    time_col = df.pop('datetime')
    df.insert(0, 'datetime', time_col)
    df = df.rename({'temp_bme': 'temp_bme (C)',
                    'press_bme': 'press_bme (hPa)',
                    'rh_bme': 'rh_bme (%)'}, axis=1)
    return df



def preprocess_cpc(file):
    df = pd.read_csv(file)
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    df['datetime'] = pd.to_datetime(df['date_time'])
    df = df.drop(['date_time'], axis=1)
    time_col = df.pop('datetime')
    df.insert(0, 'datetime', time_col)
    df = df.rename({'N conc(1/ccm)': 'N_conc_cpc(1/ccm)',
                    'Pressure (hPa)': 'press_cpc (hPa)'}, axis=1)
    return df


def preprocess_mcda(file, size):
    
    # calculate size dlog_bin
    print(size)
    mid_bin = np.fromstring(mcda_sizes[size], dtype=float, sep="\t")
    binedges = np.append(np.append(
        mid_bin[0] - (- mid_bin[0] + mid_bin[1])/2,
        (mid_bin[:-1] + mid_bin[1:])/2),
        (mid_bin[-1] - mid_bin[-2])/2 + mid_bin[-1])
    dlog_bin = np.log10(binedges[1:]) - np.log10(binedges[:-1])
    
    # Load file
    df = pd.read_csv(file, skiprows=1, header=None, dtype=str)
    df = df.iloc[:, np.r_[0:257, -6:0]]
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    df[0] = pd.to_datetime(df[0], format="%Y%m%d%H%M%S")
    df = df.rename(columns={0: 'datetime', 513: 'pcount_mcda', 514: 'pm1_mcda',
                       515: 'pm25_mcda', 516: 'pm4_mcda', 517: 'pm10_mcda', 518: 'pmtot_mcda'})
    for i in df.columns[1:-6]:
        df[i] = df[i].apply(int, base=16)
    df.columns = ['bin' + str(x) + '_mcda (dN/dlogDp)' if re.search('^[0-9]+', str(x))
                  else x for x in df.columns]
    
    for particle_size, each_dlog_bin in zip(df.columns[1:257], dlog_bin):
        df[particle_size] = df[particle_size] / each_dlog_bin / 10 / 46.67

    df = df.drop(['pcount_mcda', 'pm4_mcda', 'pmtot_mcda'], axis=1)
    return df


def preprocess_pops(file):
    df = pd.read_csv(file)
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    df['datetime'] = pd.to_datetime(df['DateTime'], unit='s') + pd.Timedelta('2hour')
    df = df.set_index('datetime').resample('1s').mean().dropna().reset_index()
    df = df.drop(['DateTime'], axis=1)
    time_col = df.pop('datetime')
    df.insert(0, 'datetime', time_col)
    
    pop_binedges = '0.119552706	0.140894644	0.169068337	0.204226949	0.227523895	0.253291842	0.279285719	0.35426882	0.604151175	0.705102841	0.785877189	1.100686925	1.117622254	1.765832382	2.690129739	3.014558062 4.392791391'
    pop_binedges = np.fromstring(pop_binedges, dtype=float, sep="\t")
    pop_midbin = (pop_binedges[1:] + pop_binedges[:-1])/2
    dlog_bin = np.log10(pop_binedges[1:]) - np.log10(pop_binedges[:-1])
    pop_binlab = ['b0', 'b1', 'b2',
                  'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11', 'b12', 'b13',
                  'b14', 'b15']

    for particle_size, each_dlog_bin in zip(pop_binlab, dlog_bin):
        df[particle_size] = df[particle_size]/(df[' POPS_Flow']*16.6667) / each_dlog_bin
    df.columns = ['bin' + str(int(x[1:]) + 1) + '_pops (dN/dlogDp)' if re.search('b[0-9]+', x)
                   else x for x in df.columns]

    df = df.drop([' Status', ' PartCt', ' BL', ' BLTH', ' STD', ' TofP', ' POPS_Flow', ' PumpFB', ' LDTemp', ' LaserFB',
                    ' LD_Mon', ' Temp', ' BatV', ' Laser_Current', ' Flow_Set',
                    'PumpLife_hrs', ' BL_Start', ' TH_Mult', ' nbins', ' logmin', ' logmax',
                    ' Skip_Save', ' MinPeakPts', 'MaxPeakPts', ' RawPts'], axis=1)
    df = df.rename({' PartCon': 'N_conc_pops (1/ccm)', ' P': 'press_pops (hPa)',
                    ' POPS_Flow': 'Flow_rate_pops (l/m)'}, axis=1)
    return df
    
    
    