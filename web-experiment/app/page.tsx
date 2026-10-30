"use client";

import { motion } from "framer-motion";
import { ArrowRight, Globe, Leaf, Zap } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        ease: [0.16, 1, 0.3, 1],
      },
    },
  };

  return (
    <div className="relative min-h-[calc(100vh-64px)] overflow-hidden">
      {/* Decorative Background Elements */}
      <div className="absolute top-0 -left-1/4 w-1/2 h-1/2 bg-brand-100/30 rounded-full blur-3xl -z-10" />
      <div className="absolute bottom-0 -right-1/4 w-1/2 h-1/2 bg-blue-100/30 rounded-full blur-3xl -z-10" />

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-7xl mx-auto px-4 pt-20 pb-32 flex flex-col items-center text-center"
      >
        <motion.div
          variants={itemVariants}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 border border-brand-100 text-brand-700 text-sm font-medium mb-8"
        >
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500"></span>
          </span>
          AI-Powered Travel Intelligence
        </motion.div>

        <motion.h1
          variants={itemVariants}
          className="text-6xl md:text-8xl font-black tracking-tight text-slate-900 mb-6 leading-[1.1]"
        >
          Wander Smarter, <br />
          <span className="bg-gradient-to-r from-brand-600 via-blue-500 to-indigo-600 bg-clip-text text-transparent">
            Not Harder.
          </span>
        </motion.h1>

        <motion.p
          variants={itemVariants}
          className="text-lg md:text-xl text-slate-600 max-w-2xl mb-12 leading-relaxed"
        >
          Next-gen travel orchestration. Personalized itineraries that respect your vibe, your goals, and our planet.
        </motion.p>

        <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4">
          <Link
            href="/build"
            className="group relative px-8 py-4 bg-slate-900 text-white rounded-2xl font-semibold overflow-hidden transition-all hover:scale-[1.02] active:scale-95"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-brand-600 to-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity" />
            <span className="relative flex items-center gap-2">
              Start Planning <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </span>
          </Link>
          <button className="px-8 py-4 bg-white text-slate-900 border border-slate-200 rounded-2xl font-semibold hover:bg-slate-50 transition-colors">
            See Example Trip
          </button>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-32 w-full"
        >
          <div className="p-8 rounded-3xl bg-white/50 border border-slate-100 backdrop-blur-sm">
            <div className="w-12 h-12 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-600 mb-6">
              <Globe className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-3 text-slate-900">Hyper-Local</h3>
            <p className="text-slate-600">Hidden gems and local secrets discovered through social media sentiment and real-time data.</p>
          </div>
          <div className="p-8 rounded-3xl bg-white/50 border border-slate-100 backdrop-blur-sm">
            <div className="w-12 h-12 bg-green-50 rounded-2xl flex items-center justify-center text-green-600 mb-6">
              <Leaf className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-3 text-slate-900">Earth-First</h3>
            <p className="text-slate-600">Low-carbon itineraries that prioritize trains and eco-friendly stays without sacrificing luxury.</p>
          </div>
          <div className="p-8 rounded-3xl bg-white/50 border border-slate-100 backdrop-blur-sm">
            <div className="w-12 h-12 bg-purple-50 rounded-2xl flex items-center justify-center text-purple-600 mb-6">
              <Zap className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-3 text-slate-900">Zero Effort</h3>
            <p className="text-slate-600">Complex logistics handled instantly. Flights, trains, and hotels orchestrated in one click.</p>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
