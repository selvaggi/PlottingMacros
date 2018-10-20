
void ratioplot1() {


   gStyle->SetOptStat(0);
   auto c1 = new TCanvas("c1", "A ratio example");

   auto h1 = new TH1D("h1", "h1", 50, 0, 10);
   auto h2 = new TH1D("h2", "h2", 50, 0, 10);

   

   f1->SetParameter(0, 3);
   h1->FillRandom("f1", 1900);
   h2->FillRandom("f1", 2000);
   h1->Sumw2();
   h2->Scale(1.9 / 2.);
   h1->GetXaxis()->SetTitle("x");
   h1->GetYaxis()->SetTitle("y");

   auto rp = new TRatioPlot(h1, h2);
   c1->SetTicks(0, 1);
   rp->Draw();
   c1->Update();


}

