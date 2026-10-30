"use client";

import { motion } from "framer-motion";
import { 
  Train, 
  MapPin, 
  Utensils, 
  Compass, 
  Leaf, 
  MessageCircle, 
  Clock, 
  Star,
  Building,
  ChevronRight,
  Zap
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Activity {
  time: string;
  name: string;
  description: string;
  sentiment: string;
}

interface Day {
  dayNumber: number;
  theme: string;
  transport?: { type: string; cost: string; details: string };
  activities: Activity[];
  dining?: { name: string; description: string; sentiment: string };
}

interface TripData {
  destination?: string;
  totalDays?: number;
  sustainabilityScore?: number;
  days?: Day[];
}

export default function ItineraryDisplay({ data }: { data: TripData }) {
  const days = data?.days || [];
  const destination = data?.destination || "Your Journey";
  const score = data?.sustainabilityScore || 0;

  return (
    <div className="space-y-12">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white border border-slate-100 p-6 rounded-3xl shadow-sm">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Destination</p>
          <p className="text-lg font-black text-slate-900 truncate">{destination}</p>
        </div>
        <div className="bg-white border border-slate-100 p-6 rounded-3xl shadow-sm">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Eco Score</p>
          <div className="flex items-center gap-2">
            <Leaf className="w-4 h-4 text-green-500" />
            <p className="text-lg font-black text-green-600">{score}/100</p>
          </div>
        </div>
        <div className="bg-white border border-slate-100 p-6 rounded-3xl shadow-sm">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Duration</p>
          <p className="text-lg font-black text-brand-600">{days.length} Days</p>
        </div>
      </div>

      {/* Timeline */}
      <div className="space-y-20 relative">
        <div className="absolute left-8 top-10 bottom-10 w-px bg-slate-100 -z-10" />
        
        {days.map((day, dIdx) => (
          <motion.div
            key={dIdx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: dIdx * 0.1 }}
          >
            {/* Day Title */}
            <div className="flex items-center gap-6 mb-10">
              <div className="w-16 h-16 rounded-[2rem] bg-slate-900 text-white flex items-center justify-center font-black text-xl shadow-xl shadow-slate-200">
                {day.dayNumber || dIdx + 1}
              </div>
              <div>
                <h3 className="text-xs font-bold text-brand-500 uppercase tracking-widest">Day {day.dayNumber || dIdx + 1}</h3>
                <h2 className="text-3xl font-black text-slate-900 tracking-tight">{day.theme || "Daily Exploration"}</h2>
              </div>
            </div>

            <div className="ml-20 space-y-8">
              {/* Transport Block (If present) */}
              {day.transport && (
                <div className="p-6 bg-blue-50/50 border border-blue-100 rounded-3xl flex gap-6 items-center">
                  <div className="w-12 h-12 bg-blue-500 rounded-2xl flex items-center justify-center text-white shrink-0 shadow-lg shadow-blue-200">
                    <Train className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-1">
                      <h4 className="font-bold text-blue-900">{day.transport.type}</h4>
                      <span className="text-[10px] font-black text-blue-600 uppercase tracking-widest bg-blue-100 px-2 py-0.5 rounded-lg">{day.transport.cost}</span>
                    </div>
                    <p className="text-blue-700/70 text-sm">{day.transport.details}</p>
                  </div>
                </div>
              )}

              {/* Activities */}
              <div className="grid grid-cols-1 gap-6">
                {day.activities?.map((act, aIdx) => (
                  <div key={aIdx} className="group bg-white border border-slate-100 rounded-[2.5rem] p-8 shadow-sm hover:shadow-xl hover:shadow-slate-200/30 transition-all">
                    <div className="flex flex-col md:flex-row gap-8">
                      <div className="w-12 h-12 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center text-slate-400 shrink-0 group-hover:bg-brand-50 group-hover:text-brand-500 transition-colors">
                        <Compass className="w-5 h-5" />
                      </div>
                      <div className="flex-1 space-y-4">
                        <div className="flex justify-between items-center">
                          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                            <Clock className="w-3 h-3" />
                            {act.time}
                          </span>
                          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-50 text-slate-500 text-[10px] font-medium border border-slate-100">
                            <MessageCircle className="w-3.5 h-3.5" />
                            {act.sentiment}
                          </div>
                        </div>
                        <h4 className="text-2xl font-black text-slate-900 group-hover:text-brand-600 transition-colors">{act.name}</h4>
                        <p className="text-slate-600 leading-relaxed text-lg">{act.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Dining Block (If present) */}
              {day.dining && (
                <div className="p-8 bg-orange-50/50 border border-orange-100 rounded-[2.5rem] flex gap-8 items-start">
                  <div className="w-14 h-14 bg-orange-500 rounded-3xl flex items-center justify-center text-white shrink-0 shadow-lg shadow-orange-200">
                    <Utensils className="w-7 h-7" />
                  </div>
                  <div className="space-y-2 flex-1">
                    <div className="flex justify-between items-center">
                      <h4 className="text-xl font-bold text-orange-900">{day.dining.name}</h4>
                      <span className="text-[10px] font-black text-orange-600 uppercase tracking-widest bg-orange-100 px-2 py-0.5 rounded-lg flex items-center gap-1">
                        <Star className="w-3 h-3 fill-current" />
                        Dining Pick
                      </span>
                    </div>
                    <p className="text-orange-800/70 leading-relaxed">{day.dining.description}</p>
                    <p className="text-[11px] italic text-orange-700 font-medium">&quot;{day.dining.sentiment}&quot;</p>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
