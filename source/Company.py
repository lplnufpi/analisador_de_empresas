class Company:

  def getNumberCNPJ(self):
    bufferCNPJ = self.cnpj
    bufferCNPJ = bufferCNPJ.replace('.','')
    bufferCNPJ = bufferCNPJ.replace('/','')
    bufferCNPJ = bufferCNPJ.replace('-','')
    return bufferCNPJ
  
  def getStringCNPJ(self):
    return self.cnpj

  def getName(self):
    return self.name

  def __init__(self,cnpj,name):
    self.cnpj = cnpj
    self.name = name
    self.capital = None
    sef.companyWeight = None

company = Company('03.079.636/0001-69','DESIGN CONSTRUCOES E EMPREENDIMENTOS LTDA')

print(company.getNumberCNPJ())