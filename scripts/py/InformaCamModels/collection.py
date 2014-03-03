import os

from asset import Asset
from j3m import J3M

class Collection(Asset):
	def __init__(self, inflate=None, _id=None, reindex=False):
		if _id is None:
			if inflate is None:
				return
			
			inflate = self.massageData(inflate)
		
		super(Collection, self).__init__(inflate=inflate, _id=_id, river="collections", extra_omits=['j3m'])
		
		if hasattr(self, "j3m_id") and self.j3m_id is not None:
			self.j3m = J3M(_id=self.j3m_id)
	
	def mergeJ3M(self):
		from submission import Submission
		if not hasattr(self, "attached_media"):
			return
			
		if not hasattr(self, "j3m"):
			self.j3m = dict(data={"sensorCapture" : []})
		
		for s in self.attached_media:
			sub = Submission(_id=s)			
			self.j3m.data['sensorCapture'].extend(sub.j3m.data['sensorCapture'])
			
			'''
			try:
				self.j3m.data['exif'].extend(sub.j3m.data['exif'])
			except:
				try:
					self.j3m.data['exif'] = sub.j3m.data['exif']
				except KeyError as e: pass
			'''
	
	def massageData(self, inflate):
		try:
			submissions = inflate['attached_media']
			from submission import Submission
			
			contributors = []
			for s in submissions:
				submission = Submission(_id=s)
				print submission.emit()
				
				contributors.append(
					submission.j3m.genealogy['createdOnDevice'])
			
			inflate['contributors'] = list(set(contributors))
			
		except KeyError as e:
			print e
			pass
		
		return inflate