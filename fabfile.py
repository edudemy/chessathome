from fabric.api import *
import sys
import os
import json
import platform
import re
import shutil
import datetime

def concat():
  local('mkdir -p build')
  filelist = os.listdir("ai")

  content = ""

  for cdir, dirs, filelist in os.walk("ai"):
    for filename in filelist:
      if (filename.endswith(".js")):
        file = open(cdir +'/'+ filename, "r")
        content += file.read()
        file.close()

  file = open("build/engine.js", "w")
  #file.write('"use strict";\n');
  file.write(content)
  file.close()

  local("git add build/")

def install():
  local('npm install')
  concat()

env.gameEngine="local"
def embed():
  env.gameEngine="local"

def dist():
  env.gameEngine = "distributed-mongo"

def serve():
  local("AI_ENGINE='%s' node --stack_size=8128 app.js" % env.gameEngine)

def test():
  for f in os.listdir("test/chess"):
    if f[0]!="_":
      print local("cd test/ && AI_ENGINE='%s' node runner.js chess/%s" % (env.gameEngine,f))

def stest(filename=None):
  print local("cd test/ && AI_ENGINE='%s' node runner.js chess/%s" % (env.gameEngine,filename))


def deploy():
  #
  local("./deploytolinode linode")

#workers & redirect
def joyentdeploy():
  local("git push joyent master")
  local("git push chessathome-worker1.no.de master")

# create a folder that will serve to publish chessathome-worker on https://github.com/joshfire/chessathome-worker
def makeworker():
  assert os.path.isdir("../chessathome-worker/")
  local('cp chessathome-worker/* ../chessathome-worker/')
  local('cp worker/client.js ../chessathome-worker')
  local("sed -i '' \"s/var ENGINE_PATH = '\.\.\/build\/engine\.js'/var ENGINE_PATH = '\.\/engine\.js'/\" ../chessathome-worker/client.js")
  local('cp build/engine.js ../chessathome-worker/')

  #add exec
  r = open("../chessathome-worker/client.js","r").read()
  w = open("../chessathome-worker/client.js","w")
  w.write("#!/usr/bin/env node\n\n")
  w.write(r)
  w.close()

  # create chessathome-worker/package.json


