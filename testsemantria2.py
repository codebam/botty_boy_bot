from __future__ import print_function, unicode_literals
import sys
import time
import uuid
import semantria

if __name__ == "__main__":
   print("Semantria Collection processing mode demo.")

   docs = []
   print("Reading collection from file...")
   for line in open('source.txt'):
      docs.append(line)

   if len(docs) < 1:
      print("Source file isn't available or blank.")
      sys.exit(1)

   session = semantria.Session("98b2c1f2-318f-4de6-a0f3-27bffd811737", "a90aa5cb-d515-4548-985c-735454a8a9a7", use_compression=True)

   collection_id = str(uuid.uuid4())
   status = session.queueCollection({"id": collection_id, "documents": docs})

   if status != 200 and status != 202:
      print("Error:")
      print(status)
      sys.exit(1)

   print("%s collection queued successfully." % collection_id)

   result = None
   while True:
      time.sleep(1)
      print("Retrieving your processed results...")
      result = session.getCollection(collection_id)
      if result['status'] != 'QUEUED':
         break
   if result['status'] != 'PROCESSED':
      print("Error:")
      print(results['status'])
      sys.exit(1)

   print("")
   for facet in result['facets']:
       print("%s : %s" % (facet['label'], facet['count']))
