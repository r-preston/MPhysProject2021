#include "Pythia8/Pythia.h"
#include "TTree.h"
#include "TFile.h"

using namespace Pythia8;

int main()
{
  Pythia pythia;
  pythia.readString("WeakSingleBoson:all = on");
  //pythia.readString("PhaseSpace:pTHatMin = 20.");
  pythia.readString("Beams:eCM = 5000.");
  pythia.init();

  TFile *file = TFile::Open("pytree.root","recreate");
  TTree *T = new TTree("z-tree","z-tree");

  float mup_PT, mup_ETA, mup_PHI;
  float mum_PT, mum_ETA, mum_PHI;
  T->Branch("mup_PT", &mup_PT );
  T->Branch("mup_ETA",&mup_ETA);
  T->Branch("mup_PHI",&mup_PHI);
  T->Branch("mum_PT", &mum_PT );
  T->Branch("mum_ETA",&mum_ETA);
  T->Branch("mum_PHI",&mum_PHI);

  Event& event = pythia.event;

  // Begin event loop. Generate event. Skip if error.
  for (int i_event = 0; i_event < 1000; ++i_event)
  {
    if (!pythia.next()) continue;

    float max_mup_pt = 0;
    int max_mup_id = -1;
    float max_mum_pt = 0;
    int max_mum_id = -1;

    for (int i_particle = 0; i_particle < event.size(); ++i_particle )
    {
      Particle &particle = event[i_particle];

      if(particle.id() == 13)
      { // particle is a muon mu-
        if(particle.pT() > max_mup_pt)
        {
          max_mup_pt = particle.pT();
          max_mup_id = i_particle;
        }
      }
      if(particle.id() == -13)
      { // particle is a antimuon mu+
        if(particle.pT() > max_mum_pt)
        {
          max_mum_pt = particle.pT();
          max_mum_id = i_particle;
        }
      }
    }

    if((max_mup_id != -1) && (max_mum_id != -1)) {
      mup_PT  = event[max_mup_id].pT();
      mup_ETA = event[max_mup_id].eta();
      mup_PHI = event[max_mup_id].phi();
      mum_PT  = event[max_mum_id].pT();
      mum_ETA = event[max_mum_id].eta();
      mum_PHI = event[max_mum_id].phi();

      T->Fill();
    }
  }

  //pythia.stat();


  //T->Print();
  T->Write();
  delete file;

  return 0;
}

