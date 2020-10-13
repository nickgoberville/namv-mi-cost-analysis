from distutils.core import setup

setup(name = "reVision",
    version = "0.1",
    description = "Core technology of Revision Autonomy",
    author = "Nick Goberville",
    author_email = "nicholas.a.goberville@wmich.edu",
    url = "Nan",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['reVision', 'reVision.access_data', 'reVision.models', 'reVision.models.ai', 'reVision.models.non_ai', 'reVision.tools'])