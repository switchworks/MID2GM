import sys
import os
import re
import glob
exec(open("./MIDIData.py",encoding='utf-8').read())

# volume magnification for each program
VolMul = [1.0]*128
VolMul[121] = 0.0

# key transpose for each program
KeyChg = [0]*128
#KeyChg[1] = -24

# PrgChg fix per song
#    0-127 : normal map
#  128-    : drum key(+128)
PrgChg = {}
#PrgChg['01'] = [121]*32 + [48,46,48]

# loop info(beat)
Loop = {}
#Loop['01'] = [0,192]
#Loop['02'] = [-1,-1]

# find src
#if os.path.isdir('./snes/rnh/'):
#	filepath = './snes/rnh/'
#elif os.path.isdir('./spc/rnh/'):
#	filepath = './spc/rnh/'
#elif os.path.isdir('./rnh/'):
#	filepath = './rnh/'
#else:
#	os._exit(0)
filepath = './'

pDrumTrack = None
files = glob.glob(filepath+"*.mid")
for file in files[:]:
	if file[-7:] != '_GM.mid':
		file = re.sub('.+\\\\', '', file)
		sid = os.path.splitext(os.path.basename(file))[0].split('_')[0]
		pMIDIData = MIDIData_LoadFromSMF(filepath+file)
		pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
		trk = 0
		lstDel = []
		while pMIDITrack:
			pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
			while pMIDIEvent:
				MIDIEvent_Combine(pMIDIEvent)
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			trk+=1
			pMIDITrack = MIDITrack_GetNextTrack(pMIDITrack)
		if Loop[sid] != [-1,-1]:
			MIDITrack_InsertMarker(MIDIData_GetFirstTrack(pMIDIData),int(Loop[sid][0]*MIDIData_GetTimeResolution(pMIDIData)),'loopStart')
			MIDITrack_InsertMarker(MIDIData_GetFirstTrack(pMIDIData),int(Loop[sid][1]*MIDIData_GetTimeResolution(pMIDIData)),'loopEnd')
		if pDrumTrack != None:
			# additional for drum track
			pMIDIEvent = MIDITrack_GetFirstEvent(pDrumTrack)
			while pMIDIEvent:
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			MIDITrack_InsertEndofTrack(pDrumTrack,MIDIEvent_GetTime(MIDITrack_GetLastEvent(pDrumTrack)))
			MIDIData_AddTrack(pMIDIData,pDrumTrack)
		# additional
		pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
		trk = 0
		lstDel = []
		while pMIDITrack:
			pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
			while pMIDIEvent:
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			trk+=1
			pMIDITrack = MIDITrack_GetNextTrack(pMIDITrack)
		MIDIData_SaveAsSMF(pMIDIData,filepath+file[:-4]+'_GM.mid')
		MIDIData_Delete(pMIDIData)
		pDrumTrack = None
