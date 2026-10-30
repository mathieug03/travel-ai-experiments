"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Loader2, CheckCircle2, Globe, Leaf, MessageCircle } from "lucide-react";
import ItineraryDisplay from "@/components/ItineraryDisplay";

const loadingSteps = [
  "Analyzing flight data and rail connections...",
  "Scanning social sentiment for hidden gems...",
  "Optimizing for Earth-First sustainability...",
  "Personalizing the vibe and goals...",
  "Finalizing your master orchestrator's plan...",
];

const mock5DayItinerary = {
  destination: "Paris & Provence",
  earthFirst: true,
  itinerary: [
    {
      day: 1,
      theme: "The City of Lights",
      activities: [
        {
          type: "transport",
          title: "Eurostar High-Speed Rail",
          detail: "Sustainable journey from London St Pancras to Paris Gare du Nord.",
          cost_estimate: "€85",
          carbon_impact: "Very Low",
          sentiment: "97% Positive - 'Stress-free travel'"
        },
        {
          type: "hotel",
          title: "Hôtel HOY Paris",
          detail: "Yoga-focused eco-hotel in the heart of the 9th arrondissement.",
          sentiment: "92% Instagrammable - 'Serene sanctuary'",
          amenities: ["Yoga Studio", "Plant-based Kitchen"]
        }
      ]
    },
    {
      day: 2,
      theme: "Local Secrets",
      activities: [
        {
          type: "activity",
          title: "Private Atelier Visit",
          detail: "Hidden artisan workshops in the Marais district.",
          sentiment: "89% Local Buzz - 'Authentic Parisian craftsmanship'",
          duration: "3 hours"
        }
      ]
    },
    {
      day: 3,
      theme: "Southward Bound",
      activities: [
        {
          type: "transport",
          title: "TGV InOui",
          detail: "Ultra-fast electric train to Avignon.",
          cost_estimate: "€45",
          carbon_impact: "Low",
          sentiment: "95% Positive - 'Scenic and fast'"
        }
      ]
    },
    {
      day: 4,
      theme: "Provencal Charm",
      activities: [
        {
          type: "restaurant",
          title: "Le Potager d'Antan",
          detail: "Garden-to-table dining in the Luberon valley.",
          sentiment: "91% Social Media Buzz - 'Unforgettable views'",
          highlight: "Zucchini Flower Tempura"
        }
      ]
    },
    {
      day: 5,
      theme: "The Grand Finale",
      activities: [
        {
          type: "activity",
          title: "Electric Bike Vineyard Tour",
          detail: "Low-impact exploration of organic vineyards.",
          sentiment: "98% Positive - 'Educational and fun'",
          duration: "5 hours"
        }
      ]
    }
  ]
};

export default function DemoPage() {
  const [step, setStep] = useState(0);
  const [showItinerary, setShowItinerary] = useState(false);

  useEffect(() => {
    if (step < loadingSteps.length) {
      const timer = setTimeout(() => {
        setStep(prev => prev + 1);
      }, 1500);
      return () => clearTimeout(timer);
    } else {
      const timer = setTimeout(() => {
        setShowItinerary(true);
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [step]);

  return (
    <div className="max-w-5xl mx-auto px-4 py-20">
      <AnimatePresence mode="wait">
        {!showItinerary ? (
          <motion.div
            key="loading"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.1 }}
            className="flex flex-col items-center justify-center min-h-[60vh] text-center"
          >
            <div className="relative mb-8">
              <div className="absolute inset-0 bg-brand-500/20 blur-3xl rounded-full" />
              <div className="relative w-24 h-24 bg-white rounded-3xl shadow-xl flex items-center justify-center border border-slate-100">
                <Loader2 className="w-10 h-10 text-brand-600 animate-spin" />
              </div>
            </div>
            
            <div className="space-y-4 max-w-md mx-auto">
              <h2 className="text-2xl font-black text-slate-900 tracking-tight">
                {step < loadingSteps.length ? "WanderAI is Orchestrating..." : "Finalizing Itinerary..."}
              </h2>
              <div className="space-y-3">
                {loadingSteps.map((text, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ 
                      opacity: step >= idx ? 1 : 0.3,
                      x: step >= idx ? 0 : -10,
                      color: step === idx ? "#0ea5e9" : step > idx ? "#64748b" : "#cbd5e1"
                    }}
                    className="flex items-center justify-center gap-3 text-sm font-medium"
                  >
                    {step > idx ? <CheckCircle2 className="w-4 h-4 text-green-500" /> : <div className="w-4 h-4 rounded-full border border-current opacity-30" />}
                    {text}
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="itinerary"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            <div className="flex flex-col md:flex-row justify-between items-center gap-6 bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-xl shadow-slate-200/50 mb-12">
              <div className="text-center md:text-left">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 text-brand-700 text-xs font-bold mb-3 uppercase tracking-wider">
                  Visual Demo
                </div>
                <h1 className="text-4xl font-black text-slate-900">{mock5DayItinerary.destination}</h1>
                <p className="text-slate-500 mt-2 font-medium">5-Day Sustainable Masterpiece</p>
              </div>
              <div className="flex gap-4">
                <div className="text-center px-6 py-3 bg-slate-50 rounded-2xl border border-slate-100">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Carbon</div>
                  <div className="text-xl font-black text-green-600">-84%</div>
                </div>
                <div className="text-center px-6 py-3 bg-slate-50 rounded-2xl border border-slate-100">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Social</div>
                  <div className="text-xl font-black text-brand-600">94.8</div>
                </div>
              </div>
            </div>
            
            <ItineraryDisplay data={mock5DayItinerary as any} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
