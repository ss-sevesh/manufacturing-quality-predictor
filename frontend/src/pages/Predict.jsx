import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import toast from 'react-hot-toast';
import { usePredict } from '../hooks/usePredictions';
import { getScoreClasses, getScoreBorder } from '../utils/helpers';
import { Send, Shuffle } from 'lucide-react';

const schema = z.object({
  temperature: z.coerce.number().min(100).max(300),
  pressure: z.coerce.number().min(20).max(80),
  humidity: z.coerce.number().min(10).max(100),
  speed: z.coerce.number().min(500).max(2000),
  vibration: z.coerce.number().min(0).max(1),
  thickness: z.coerce.number().min(0.5).max(5),
  power_consumption: z.coerce.number().min(200).max(500),
  tool_wear: z.coerce.number().min(0).max(1),
  coolant_flow: z.coerce.number().min(0).max(20),
  ambient_temp: z.coerce.number().min(10).max(45),
  cycle_time: z.coerce.number().min(20).max(80),
  material_hardness: z.coerce.number().min(30).max(80),
  spindle_load: z.coerce.number().min(20).max(100),
  feed_rate: z.coerce.number().min(0.05).max(0.5),
  surface_roughness: z.coerce.number().min(0).max(20),
});

const fieldRanges = {
  temperature:       { min: 100,  max: 300,  decimals: 1 },
  pressure:          { min: 20,   max: 80,   decimals: 1 },
  humidity:          { min: 10,   max: 100,  decimals: 1 },
  speed:             { min: 500,  max: 2000, decimals: 0 },
  vibration:         { min: 0,    max: 1,    decimals: 3 },
  thickness:         { min: 0.5,  max: 5,    decimals: 2 },
  power_consumption: { min: 200,  max: 500,  decimals: 1 },
  tool_wear:         { min: 0,    max: 1,    decimals: 3 },
  coolant_flow:      { min: 0,    max: 20,   decimals: 2 },
  ambient_temp:      { min: 10,   max: 45,   decimals: 1 },
  cycle_time:        { min: 20,   max: 80,   decimals: 1 },
  material_hardness: { min: 30,   max: 80,   decimals: 1 },
  spindle_load:      { min: 20,   max: 100,  decimals: 1 },
  feed_rate:         { min: 0.05, max: 0.5,  decimals: 3 },
  surface_roughness: { min: 0,    max: 20,   decimals: 2 },
};

function randomValues() {
  return Object.fromEntries(
    Object.entries(fieldRanges).map(([key, { min, max, decimals }]) => {
      const val = min + Math.random() * (max - min);
      return [key, +val.toFixed(decimals)];
    })
  );
}

const fields = [
  { name: 'temperature', label: 'Temperature (C)', placeholder: '185' },
  { name: 'pressure', label: 'Pressure (bar)', placeholder: '45' },
  { name: 'humidity', label: 'Humidity (%)', placeholder: '62' },
  { name: 'speed', label: 'Speed (RPM)', placeholder: '1200' },
  { name: 'vibration', label: 'Vibration (mm/s)', placeholder: '0.03' },
  { name: 'thickness', label: 'Thickness (mm)', placeholder: '2.5' },
  { name: 'power_consumption', label: 'Power (W)', placeholder: '340' },
  { name: 'tool_wear', label: 'Tool Wear (0-1)', placeholder: '0.15' },
  { name: 'coolant_flow', label: 'Coolant Flow (L/min)', placeholder: '8.5' },
  { name: 'ambient_temp', label: 'Ambient Temp (C)', placeholder: '24' },
  { name: 'cycle_time', label: 'Cycle Time (s)', placeholder: '45' },
  { name: 'material_hardness', label: 'Hardness (HRC)', placeholder: '58' },
  { name: 'spindle_load', label: 'Spindle Load (%)', placeholder: '72' },
  { name: 'feed_rate', label: 'Feed Rate (mm/rev)', placeholder: '0.25' },
  { name: 'surface_roughness', label: 'Surface Roughness (um)', placeholder: '1.2' },
];

export default function Predict() {
  const { register, handleSubmit, reset, formState: { errors } } = useForm({ resolver: zodResolver(schema) });
  const mutation = usePredict();

  const onSubmit = (data) => {
    mutation.mutate(data, {
      onSuccess: () => toast.success('Prediction complete'),
      onError: () => toast.error('Prediction failed'),
    });
  };

  const result = mutation.data;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Predict Quality</h2>
        <p className="text-gray-500 dark:text-gray-400">Enter manufacturing parameters to predict quality score</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {fields.map(({ name, label, placeholder }) => (
          <div key={name}>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{label}</label>
            <input
              type="number"
              step="any"
              placeholder={placeholder}
              {...register(name)}
              className={`w-full rounded-lg border px-3 py-2 text-sm bg-white dark:bg-gray-800 dark:text-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors[name] ? 'border-red-400 dark:border-red-500' : 'border-gray-300 dark:border-gray-700'
              }`}
            />
            {errors[name] && <p className="mt-1 text-xs text-red-500">{errors[name].message}</p>}
          </div>
        ))}

        <div className="md:col-span-2 lg:col-span-3 pt-2 flex gap-3">
          <button
            type="submit"
            disabled={mutation.isPending}
            className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            <Send size={16} />
            {mutation.isPending ? 'Predicting...' : 'Predict Quality'}
          </button>
          <button
            type="button"
            onClick={() => reset(randomValues())}
            className="inline-flex items-center gap-2 rounded-lg border border-gray-300 dark:border-gray-700 px-6 py-2.5 text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <Shuffle size={16} />
            Fill Random
          </button>
        </div>
      </form>

      {result && (
        <div className={`rounded-xl border-2 p-8 text-center transition-all animate-in fade-in ${getScoreBorder(result.quality_score)} bg-white dark:bg-gray-900`}>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Predicted Quality Score</p>
          <p className="text-6xl font-bold tracking-tighter mb-3">{result.quality_score.toFixed(1)}</p>
          <span className={`inline-block rounded-full px-4 py-1.5 text-sm font-bold uppercase ${getScoreClasses(result.quality_score)}`}>
            {result.status}
          </span>
          <p className="mt-3 text-sm text-gray-500 dark:text-gray-400">Confidence: {(result.confidence * 100).toFixed(0)}%</p>
        </div>
      )}
    </div>
  );
}
