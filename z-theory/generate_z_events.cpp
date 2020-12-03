#include "Pythia8/Pythia.h"
#include "TTree.h"
#include "TFile.h"

using namespace Pythia8;

int main()
{
  Pythia pythia;
  pythia.readString("WeakSingleBoson:all = on");
  //pythia.readString("PhaseSpace:pTHatMin = 20.");
  //pythia.readString("PhaseSpace:pTHatMax = 200.");
  pythia.readString("Beams:eCM = 5000.");
  pythia.init();

  TFile *file = TFile::Open("zmuons.root","recreate");
  TTree *T = new TTree("mutree","Muon Tree");
  TTree *Txsec = new TTree("xtree","X-Section Tree");

  float mup_PT, mup_ETA, mup_PHI;
  float mum_PT, mum_ETA, mum_PHI;
  T->Branch("mup_PT", &mup_PT );
  T->Branch("mup_ETA",&mup_ETA);
  T->Branch("mup_PHI",&mup_PHI);
  T->Branch("mum_PT", &mum_PT );
  T->Branch("mum_ETA",&mum_ETA);
  T->Branch("mum_PHI",&mum_PHI);

  float weight, num_generated, total_cross_section, numerical_error;
  Txsec->Branch("weight", &weight);
  Txsec->Branch("num_generated", &num_generated);
  Txsec->Branch("total_cross_section", &total_cross_section);
  Txsec->Branch("numerical_error", &numerical_error);

  long events_generated = 0;

  Event& event = pythia.event;

  // Begin event loop. Generate event. Skip if error.
  for (int i_event = 0; i_event < 10000; ++i_event)
  {
    if (!pythia.next()) continue;

    events_generated++;

    float max_mup_pt = 0;
    int max_mup_id = -1;
    float max_mum_pt = 0;
    int max_mum_id = -1;

    for (int i_particle = 0; i_particle < event.size(); ++i_particle )
    {
      Particle &particle = event[i_particle];

      if(particle.id() == -13)
      { // particle is a antimuon mu+
        if(particle.pT() > max_mup_pt)
        {
          max_mup_pt = particle.pT();
          max_mup_id = i_particle;
        }
      }
      if(particle.id() == 13)
      { // particle is a muon mu-
        if(particle.pT() > max_mum_pt)
        {
          max_mum_pt = particle.pT();
          max_mum_id = i_particle;
        }
      }
    }

    if((max_mup_id != -1) && (max_mum_id != -1)) {

      /*if((max_mup_pt < 20) || (max_mum_pt < 20)) {
        continue;
      }*/
      mup_PT  = event[max_mup_id].pT();
      mup_ETA = event[max_mup_id].eta();
      mup_PHI = event[max_mup_id].phi();
      mum_PT  = event[max_mum_id].pT();
      mum_ETA = event[max_mum_id].eta();
      mum_PHI = event[max_mum_id].phi();

      T->Fill();
    }
  }

  T->Write();

  // cross section weight per particle (factor of 1e9 converts from mb to pb)
  num_generated = events_generated;
  total_cross_section = pythia.info.sigmaGen() * 1e9;
  numerical_error = pythia.info.sigmaErr() * 1e9;
  weight = total_cross_section / num_generated;

  Txsec->Fill();
  Txsec->Write();

  //pythia.stat();

  delete file;

  return 0;
}

