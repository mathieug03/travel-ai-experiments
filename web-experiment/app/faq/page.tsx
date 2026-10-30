"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, Sparkles, Leaf, Globe, Search } from "lucide-react";

const faqs = [
  {
    question: "How does WanderAI actually work?",
    answer: "WanderAI leverages advanced LLMs (Mistral) orchestrated with real-time travel data. We analyze your 'vibe' and 'goals' to match you with destinations and experiences that aren't just popular, but personally resonant. Our engine cross-references social sentiment with logistics to ensure a seamless trip.",
    icon: <Sparkles className="w-5 h-5 text-brand-500" />
  },
  {
    question: "What are your data sources?",
    answer: "We aggregate data from multiple premium sources: real-time flight and rail APIs (like Duffel and Trainline), Google Places for venue details, and—most importantly—social media sentiment analysis from platforms like TikTok and Instagram to identify 'hidden gems' before they become overcrowded.",
    icon: <Globe className="w-5 h-5 text-blue-500" />
  },
  {
    question: "What is 'Earth-First' mode?",
    answer: "This is our signature low-carbon feature. When enabled, our algorithm prioritizes high-speed rail over short-haul flights and recommends 'Eco-Luxe' certified stays. We calculate the carbon footprint for every leg of your journey, ensuring your wanderlust doesn't cost the planet.",
    icon: <Leaf className="w-5 h-5 text-green-500" />
  },
  {
    question: "Can I book directly through WanderAI?",
    answer: "Currently, WanderAI is your master orchestrator and planner. We provide direct links to booking platforms for each segment of your itinerary. A unified, one-click booking experience is coming in our v2 release later this year.",
    icon: <Search className="w-5 h-5 text-purple-500" />
  }
];

function AccordionItem({ item, isOpen, onClick }: { item: typeof faqs[0], isOpen: boolean, onClick: () => void }) {
  return (
    <div className="border-b border-slate-100 last:border-0">
      <button
        onClick={onClick}
        className="w-full py-6 flex items-center justify-between text-left focus:outline-none group"
      >
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center group-hover:bg-brand-50 transition-colors">
            {item.icon}
          </div>
          <span className="text-lg font-bold text-slate-900">{item.question}</span>
        </div>
        <ChevronDown className={`w-5 h-5 text-slate-400 transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`} />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <p className="pb-6 pl-14 text-slate-600 leading-relaxed max-w-3xl">
              {item.answer}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function FAQPage() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <div className="max-w-4xl mx-auto px-4 py-20">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-16"
      >
        <h1 className="text-4xl md:text-5xl font-black text-slate-900 mb-4">Frequently Asked Questions</h1>
        <p className="text-slate-500 text-lg">Everything you need to know about the future of travel.</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-[2.5rem] p-8 md:p-12 shadow-xl shadow-slate-200/50 border border-slate-100"
      >
        {faqs.map((faq, index) => (
          <AccordionItem
            key={index}
            item={faq}
            isOpen={openIndex === index}
            onClick={() => setOpenIndex(openIndex === index ? null : index)}
          />
        ))}
      </motion.div>
    </div>
  );
}
