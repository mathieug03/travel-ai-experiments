"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Send, 
  MapPin, 
  Users, 
  Sparkles, 
  Leaf, 
  Info, 
  ChevronDown, 
  Loader2,
  Train,
  Plane,
  Building,
  Utensils,
  Calendar
} from "lucide-react";
import ItineraryDisplay from "@/components/ItineraryDisplay";
import SatisfactionRating from "@/components/SatisfactionRating";

export default function TripBuilder() {
  const [loading, setLoading] = useState(false);
  const [itinerary, setItinerary] = useState<any>(null);
  const [earthFirst, setEarthFirst] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    try {
      const response = await fetch("/api/generate-trip", {
        method: "POST",
        body: JSON.stringify({
          destination: (e.target as any).destination.value,
          duration: (e.target as any).duration.value,
          context: (e.target as any).context.value,
          vibe: (e.target as any).vibe.value,
          earthFirst,
        }),
      });
      const data = await response.json();
      console.log("WanderAI API Raw Response:", data);
      setItinerary(data);
    } catch (error) {
      console.error("Failed to generate itinerary:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <AnimatePresence mode="wait">
        {!itinerary ? (
          // ... existing form code ...
          <motion.div
            key="form"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white rounded-[2.5rem] p-8 md:p-12 shadow-xl shadow-slate-200/50 border border-slate-100"
          >
            <div className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 bg-brand-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-brand-200">
                <Sparkles className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Plan Your Journey</h1>
                <p className="text-slate-500">Let WanderAI orchestrate your perfect escape.</p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Destination */}
                <div className="md:col-span-1 space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-brand-500" />
                    Destination
                  </label>
                  <input
                    required
                    name="destination"
                    placeholder="Tokyo, etc."
                    className="w-full px-5 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all placeholder:text-slate-400"
                  />
                </div>

                {/* Duration */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-brand-500" />
                    Duration
                  </label>
                  <input
                    required
                    type="number"
                    name="duration"
                    min="1"
                    max="14"
                    defaultValue="3"
                    className="w-full px-5 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all"
                  />
                </div>

                {/* Context */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                    <Users className="w-4 h-4 text-brand-500" />
                    Context
                  </label>
                  <div className="relative">
                    <select
                      name="context"
                      className="w-full appearance-none px-5 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all text-slate-700"
                    >
                      <option value="solo">Solo</option>
                      <option value="couple">Couple</option>
                      <option value="family">Family</option>
                      <option value="friends">Friends</option>
                    </select>
                    <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                  </div>
                </div>
              </div>

              {/* Vibe & Goals */}
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-brand-500" />
                  Vibe & Goals
                </label>
                <textarea
                  required
                  name="vibe"
                  rows={4}
                  placeholder="Tell us what you love (e.g., Sightseeing, nature, food, hidden architecture gems...)"
                  className="w-full px-5 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all placeholder:text-slate-400 resize-none"
                />
              </div>

              {/* Earth-First Toggle */}
              <div className="p-6 rounded-3xl bg-green-50/50 border border-green-100/50">
                <div className="flex items-center justify-between">
                  <div className="flex gap-4">
                    <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center text-green-600">
                      <Leaf className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900">Earth-First Mode</h3>
                      <p className="text-sm text-slate-600 max-w-md mt-1">
                        Prioritizes train travel and low-carbon footprint itineraries.
                      </p>
                    </div>
                  </div>
                  
                  <button
                    type="button"
                    onClick={() => setEarthFirst(!earthFirst)}
                    className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors focus:outline-none ${
                      earthFirst ? "bg-green-500" : "bg-slate-200"
                    }`}
                  >
                    <motion.span
                      animate={{ x: earthFirst ? 28 : 4 }}
                      className="inline-block h-6 w-6 transform rounded-full bg-white shadow-sm"
                    />
                  </button>
                </div>
              </div>

              <button
                disabled={loading}
                className="w-full group relative px-8 py-5 bg-slate-900 text-white rounded-3xl font-bold text-lg overflow-hidden transition-all hover:scale-[1.01] active:scale-[0.99] disabled:opacity-70 disabled:hover:scale-100 shadow-xl shadow-slate-200"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-brand-600 to-brand-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                <span className="relative flex items-center justify-center gap-2">
                  {loading ? (
                    <>
                      <Loader2 className="w-6 h-6 animate-spin" />
                      Crafting Your Journey...
                    </>
                  ) : (
                    <>
                      Generate Itinerary <Send className="w-5 h-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                    </>
                  )}
                </span>
              </button>
            </form>
          </motion.div>
        ) : (
          <motion.div
            key="itinerary"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            <div className="flex justify-between items-center bg-white p-6 rounded-3xl border border-slate-100 shadow-sm mb-8">
              <div>
                <p className="text-sm font-medium text-slate-500">Your Journey to</p>
                <h2 className="text-2xl font-black text-slate-900">{itinerary.destination || "Discovery"}</h2>
              </div>
              <button 
                onClick={() => setItinerary(null)}
                className="px-5 py-2 text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors"
              >
                Start Over
              </button>
            </div>
            
            <ItineraryDisplay data={itinerary} />
            <SatisfactionRating />

            {/* DEBUG BOX */}
            <div className="mt-12 p-6 bg-slate-900 rounded-3xl overflow-hidden">
              <h3 className="text-brand-400 text-xs font-bold uppercase tracking-widest mb-4">Raw API Debug Output</h3>
              <pre className="text-slate-300 text-[10px] font-mono overflow-auto max-h-96 custom-scrollbar">
                {JSON.stringify(itinerary, null, 2)}
              </pre>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
