import os
import configparser


def section_key_loader(section, sectionKey, default=''):
    section = section.upper()
    sectionKey = sectionKey.upper()
    config = configparser.ConfigParser()   
    try:
        config.read('Config.ini')
        item = config[section][sectionKey]
        return item
    except (configparser.ParsingError, KeyError, TypeError) as e:
        with open('Config.ini', 'w') as configFile:
            try:
                if section not in config.sections():
                    config.add_section(section)
                config[section][sectionKey] = str(default)
                config.write(configFile)  
            except (configparser.NoSectionError) as e:
                print(f'error {e}')
            return default


def section_key_writer(section, sectionKey, value):
    section = section.upper()
    sectionKey = sectionKey.upper()
    config = configparser.ConfigParser()
    config.read('Config.ini')
    with open('Config.ini', 'w') as config_file:
        try:
            if section not in config.sections():
                config.add_section(section)
            config.set(section, sectionKey, value)
            config.write(config_file)
        except Exception as error:
            print(f'error {error}')
        return


def section_eraser(section):
    section = section.upper()
    config = configparser.ConfigParser()
    config.read('Config.ini')
    with open('Config.ini', 'w') as config_file:
        try:
            if section not in config.sections():
                return
            else:
                config.remove_section(section)
                return
        except Exception as error:
            print(f'error {error}')


def ConfigLoader(Section, SectionKey):
    config = configparser.ConfigParser()
    if os.path.isfile('Config.ini'):
        try:
            config.read('Config.ini')
            itemsList = list(filter(None, config[Section][SectionKey].split(',\n')))
            return itemsList
        except (configparser.ParsingError, KeyError) as e:
            with open('Config.ini', 'w') as configFile:
                try:
                    for opt in config.items(Section):
                        if SectionKey.__eq__(opt[0]):
                            config.remove_option(Section, SectionKey)
                except (configparser.NoSectionError) as e:
                    config.add_section(Section)
                config.write(configFile)    
    itemsList = DefaultItemsList(Section, SectionKey)
    config.set(Section, SectionKey, (',\n'.join([str(itemName) for itemName in itemsList])))
    with open('Config.ini', 'w') as configFile:
        for conf in config:
            for item in config.items(conf):
                print(f'{conf} {item[0]}')
        config.write(configFile)
    return itemsList

            
        
# ParsingError
# KeyError
#    Create Section
# Temp main



# config['Breakage'] = {'List' : ',\n'.join([str(breakageName) for breakageName in BreakageList])}

# with open('Config.ini', 'w') as configfile:
#     config.write(configfile)

    # config.read('Config.ini')
    # BreakageString = config['Breakage']['List']
    # breakageList = list(filter(None, BreakageString.split(',\n')))   
    # print(breakageList)


# ================================================================================================================
#                                               Internal Functions
# ================================================================================================================

# INI File
#   Breakage
#       BreakageList
#       BreakageFilePath



def DefaultItemsList(sectionName, SectionKey):
    StringDict = {}
    StringDict['Breakage'] = {'list' : '''
PFF- SEPARAÇÃO ERRADA
PFF-ABERTO PERDA ERRADA
PFF-ALTA COMPLEXIDADE
PES-BASE ERRADA
PFF-BATIDA
PES-BATIDA ESTOQUE
PFF-BATIDA LASER
PFF-BATIDA POLIMENTO
PFF-BLOCAGEM
PFF-BORDA QUEBRADA
PFF-CÁLCULO
PFF-COMPLEXIDADE DO PRISMA
PFF-CORTE ERRADO GERADOR
PFF-DESBLOCAGEM NO GERADOR
PFF-DESBLOCAGEM NO POLIMENTO
PFF-DESCONFIGURAÇÃO LASER
PFF-DIOPTRIA
PFF-DUPLICIDADE
PFF-ERRO CALIBRAÇÃO
PFF-ERRO MANUTENÇÃO
PFF-FALTA DIAMETRO
PFF-FOTO NÃO ATIVA
PFF-IDENTIFICAÇÃO ERRADA
PFF-INVERTIDA POLIDORA
PFF-INVERTIDO NO LAB
PFF-LAPIDADO DEMAIS POLIMENTO
PFF-LASER DUPLO
PFF-LASER FALHADO
PFF-LASER FORTE
PFF-LASER FRACO
PFF-LASER INVERTIDO
PFF-LASER POSIÇÃO ERRADA
PFF-LENTE PERDIDA
PFF-MANCHA ACETONA
PFF-MANCHA CANETA
PFF-MANCHA OLEO GERADOR
PFF-MARCA GERADOR-BORDA
PFF-MARCA GERADOR-CENTRO
PFF-MARCA GERADOR-CÍRCULOS
PFF-POLARIZADO POSICAO ERRADA
PFF-PRODUTO ERRADO
PFF-PRODUZIDO OLHO ERRADO
PFF-QUEBRA
PFF-QUEBRA DESBLOCAGEM
PFF-QUEBRA GERADOR
PFF-RISCO
PFF-SEPARADO ERRADO ESTOQUE
PFF-TESTE LASER
'''}

    StringDict['Rework'] = {'list' : '''
RFF-BATIDA
RFF-BORDA QUEBRADA
RFF-DEFEITO MATERIAL
RFF-DESBLOCAGEM NO POLIMENTO
RFF-DEVOLUÇÃO AUTOMAPPER
RFF-DIOPTRIA
RFF-LASER DUPLO
RFF-LASER FALHADO
RFF-LASER FORTE
RFF-LASER FRACO
RFF-MARCA CANETA
RFF-MARCA GERADOR-BORDA
RFF-MARCA GERADOR-CENTRO
RFF-MARCA POLIMENTO CENTRO
RFF-RISCO
'''}

    StringDict['Blanks'] = {'blankValue' : '''
1.49:5.00
1.49 FOTO:10.00
1.56 FOTO:15.00
1.59:5.00
'''}

    StringDict['Blanks'].update({'blankAndCode' : '''
4001	MP 1.49 VS INC 68MM
4002	MP 1.49 VS INC 76MM (ZEISS) zerar p/ desat
4003	MP 1.49 VS TRANS 7 CINZA (Y)
4009	MP 1.49 VS TRANS 7 MARROM (ESSILOR)
4010	MP 1.49 VS TRANS 7 XTRACTIVE (ESSILOR)
4011	MP 1.49 VS INC PUCK 76 (ZEISS)
4013	MP 1.59 VS INC PUCK (ZEISS)
4023	MP 1.49 VS POLAR CINZA ESP.AZUL (VISION EASE)
4024	MP 1.49 VS POLAR CINZA ESP.PRATA (VISION EASE)
4026	MP 1.59 POLAR & TRANS DRIVEWEAR
4027	MP 1.67 VS UV+ 75MM HC(RENOVATE)
4031	MP 1.61 VS INC (RENOVATE)
4034	MP 1.56 VS FOTO (RENOVATE)
4039	MP 1.49 VS POLAR CINZA (VISION EASE)
4040	MP 1.49 VS POLAR VERDE (VISION EASE)
4042	MP 1.74 VS TRANS 7 CINZA (YOUNGER)
4047	MP 1.49 VS POLAR TRANS (YOUNGER)
4051	MP 1.59 VS INC 73MM (A SEPARAR)
4053	MP 1.59 VS INC 75 (VISION EASE)
4055	MP 1.59 VS POLAR UV+ CINZA (RENOVATE)
4056	MP 1.59 VS POLAR UV+ MARROM (RENOVATE)
4057	MP 1.59 VS POLAR VERDE (YOUNGER)
4058	MP 1.59 VS POLAR CINZA (YOUNGER)
4059	MP 1.59 VS POLAR CINZA UV+ ESP.PRATA (RENOVATE)
4060	MP 1.59 VS POLAR CINZA UV+ ESP.AZUL (RENOVATE)
4061	MP 1.59 VS FOTO (A SEPARAR)
4064	MP 1.59 PR POLI FOTO (RENOVATE)
4075	MP 1.59 PR INC (RENOVATE)
4077	MP 1.59 LENTE PROG SEMI ACAB ILLUMINA LIFE RX
4082	MP 1.49 PR SMALL
4083	MP PR NO LINE 80
4084	MP 1.60 PR INC ALT18MM (HOYA)
4085	MP 1.49 VS INC (ESSILOR)
4086	MP 1.49 VS ACCLIMATES (ESSILOR)
4087	MP 1.59 VS INC TINTÁVEL (RENOVATE)
4088	MP 1.59 VS UV+ HC (CB)
4089	MP 1.67 VS FOTO 70MM (CB)
4090	MP 1.67 VS UV+ 70MM HC (CB)
4091	MP 1.59 VS POLAR MARROM (YOUNGER)
4092	MP 1.56 NIGHT VISION UNC
4093	MP 1.59 VS INC - BENEFICIAMENTO FT
4094	MP 1.59 UV+ VS INC - BENEFICIAMENTO FT
4100	MP 1.59 VS TRANS 7 CINZA (ESSILOR)
4101	MP 1.59 VS TRANS 7 CINZA (YOUNGER)
4102	MP 1.56 VS UV+ (WHASHIN)
4104	MP 1.67 VS INC (WHASHIN)
4105	MP 1.67 VS INC (ZEISS)
4107	MP 1.67 VS INC (YOUNGER)
4108	MP 1.67 VS INC (ULTRA)
4109	MP 1.67 VS INC (GBO)
4110	MP 1.74 VS INC (CB)
4111	MP 1.74 VS INC (YOUNGER)
4112	MP 1.74 VS INC (GBO)
4114	MP 1.53 VS INC (YOUNGER)
4115	MP 1.53 VS INC (HOYA)
4116	MP 1.53 VS TRANS 7 CINZA (YOUNGER)
4117	MP 1.53 VS TRANS 7 CINZA (HOYA)
4118	MP 1.67 VS TRANS 7 CINZA (YOUNGER)
4120	MP 1.67 VS TRANS 7 CINZA (HOYA)
4121	MP 1.59 VS FOTO (RENOVATE)
4122	MP 1.59 VS INC FOTO (VISION EASE)
4123	MP 1.59 VS FOTO (ZEISS)
4124	MP 1.59 VS FOTO (CB)
4125	MP 1.59 VS FOTO (ULTRA)
4126	MP 1.59 VS FOTO (YOUNGER)
4127	MP 1.59 VS FOTO (GBO)
4128	MP 1.67 VS FOTO (CB)
4129	MP 1.67 VS FOTO (YOUNGER)
4130	MP 1.59 VS INC 76MM (ESSILOR)
4134	MP 1.59 VS INC 75MM (CB )
4135	MP 1.61 VS INC (YOUNGER)
4136	MP 1.67 VS UV+ (ULTRA)
4137	MP 1.59 VS FOTO (VISCO)
4138	MP 1.49 CAMBER INC (Y)
4139	MP 1.59 CAMBER INC (Y)
4140	MP 1.67 CAMBER INC (Y)
4141	MP 1.49 CAMBER TRANS (Y)
4142	MP 1.67 CAMBER TRANS (Y)
4143	MP 1.49 VS UV+ 75MM (CB)
4144	MP 1.59 UV+ VS HC FOTO (CB)
4146	MP 1.67 VS FOTO HC 75mm (CB)
4147	MP 1.74 VS UV+ UNC. (CB)
4148	MP 1.74 VS FOTO HC (CB)
4149	MP 1.49 VS INC 80MM(PEREGO)
4150	MP 1.49 VS INC 85MM(PEREGO)
4151	MP 1.49 INC SMART (O.P)
4152	MP 1.56 BF EXECUTIVE (O.P)
4153	MP 1.67 BF EXECUTIVE (O.P)
4154	MP 1.67 INC SMART (O.P)
4155	MP 1.49 VS UNC. 70mm (CB)
4156	MP 1.59 VS UV+ UNC. (CB)
4157	MP 1.67 VS UV+ UNC. 70MM (CB)
4158	MP 1.56 VS UV+ UNC (CB)
4159	MP 1.49 VS UNC. 75MM (CB)
4160	MP 1.59 VS HC (CB)
4161	MP 1.56 FOTO (J)
4162	MP 1.49 VS FOTO(M)
4163	MP 1.49 VS UNC 70mm (CT)
4164	LENTE SEMI ACABADA 1.74 UV+ HC
4165	MP 1.56 UV+ FOTO (ULTRA)
4166	MP 1.49 VS FOTO 70M (CT)
4167	MP 1.67 VS HC TINTAVEL (MR 10 MELLO)
4168	MP 1.67 VS UV+ HC 75mm (MR10 MELLO)
4177	MP 1.74 VS FOTO HC (M)
4178	MP 1.74 VS UV+ (M)
4179	MP 1.59 VS FOTO (M)
4180	MP 1.56 VS UV+ FOTO
4181	MP 1.49 VS UNC 75mm (CT)
4182	MP 1.74 CAMBER INC (Y)
4185	MP 1.74 CAMBER TRAN (Y)
'''})

    StringDict['Warranty'] = {'Motive' : '''
G-BASE ERRADA
G-DIAMETRO INSUFICIENTE
G-DIOPTRIA ERRADA
G-ERRO CALCULO
G-ESPESSURA ERRADA
G-LASER FORTE
G-LASER MARCA PROPRIA
G-LENTE QUEBRADA/LASCADA
G-NÃO ADAPTAÇÃO - INTERM E PER
G-NÃO ADAPTAÇÃO - LATERAIS
G-NÃO ADAPTAÇÃO - LONGE
G-NAO ADAPTAÇÃO - LONGE E INTE
G-NÃO ADAPTAÇÃO - LONGE E PERT
G-NÃO ADAPTAÇÃO - PERTO
'''}

    StringDict['Warranty'].update({'Adaptation' : '''
G-NÃO ADAPTAÇÃO - LONGE
G-NÃO ADAPTAÇÃO - PERTO
G-NÃO ADAPTAÇÃO - LONGE E PERT
G-NÃO ADAPTAÇÃO - LATERAIS
G-NAO ADAPTAÇÃO - LONGE E INTE
G-NÃO ADAPTAÇÃO - INTERM E PER
G-REJEIÇÃO DE MATERIAL
G-REJEIÇÃO AO SLIM
'''})

    return list(filter(None, StringDict[sectionName][SectionKey].split('\n')))

