"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Star, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

export default function SatisfactionRating() {
  const [rating, setRating] = useState<number | null>(null);
  const [hovered, setHovered] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);

  const handleRate = (value: number) => {
    setRating(value);
    setSubmitted(true);
  };

  return (
    <div className="mt-20 pt-12 border-t border-slate-100 flex flex-col items-center">
      <AnimatePresence mode="wait">
        {!submitted ? (
          <motion.div
            key="rating"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="flex flex-col items-center gap-6"
          >
            <div className="text-center">
              <h3 className="text-xl font-bold text-slate-900 mb-1">How did we do?</h3>
              <p className="text-slate-500 text-sm">Your feedback helps refine the orchestrator.</p>
            </div>
            
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onMouseEnter={() => setHovered(star)}
                  onMouseLeave={() => setHovered(null)}
                  onClick={() => handleRate(star)}
                  className="p-2 transition-all hover:scale-110 active:scale-90"
                >
                  <Star
                    className={cn(
                      "w-8 h-8 transition-colors duration-300",
                      (hovered !== null ? star <= hovered : star <= (rating || 0))
                        ? "fill-brand-500 text-brand-500"
                        : "fill-transparent text-slate-300"
                    )}
                  />
                </button>
              ))}
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="thanks"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center gap-4 py-8"
          >
            <div className="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center text-green-500 mb-2">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <div className="text-center">
              <h3 className="text-2xl font-black text-slate-900">Thank you!</h3>
              <p className="text-slate-500">Your feedback has been recorded.</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
