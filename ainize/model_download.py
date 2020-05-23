import stanza
import argparse
from prepare_resources import default_treebanks

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--server')
  args = parser.parse_args()

  end = None 
  args.server = int(args.server)

  if (args.server + 1) * 10 < len(default_treebanks):
    end = (args.server + 1) * 10
  else:
    end = len(default_treebanks)
  
  print(type(end), end)

  for idx in list(default_treebanks.keys())[args.server * 10:end]:
    stanza.download(idx, './models')
      