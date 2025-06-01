<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Illuminate\Support\Facades\Log;

class NetworkScanController extends Controller
{
    public function scan(Request $request)
    {
        $request->validate([
            'protocol' => 'required|string',
        ]);

        $protocol = $request->input('protocol');

        // Ottieni il percorso alla directory public e risali per trovare la root del progetto
        $publicPath = public_path();
        // Risali due livelli: da public/ a backend/ a domoTek/
        $projectRoot = dirname(dirname($publicPath));

        // Costruisci il percorso assoluto allo script protocol_handler.py
        $scriptPath = $projectRoot . '/scripts/protocol_handler.py';

        // Log the resolved script path for debugging
        Log::info('Resolved script path (using public_path): ' . $scriptPath);

        // Comando da eseguire. Passiamo il nome del protocollo come argomento.
        // Usiamo il percorso completo allo script e impostiamo la directory di lavoro al projectRoot.
        $process = new Process(['python', $scriptPath, $protocol], $projectRoot);

        try {
            $process->run();

            // Esegue l'output solo se il processo ha avuto successo
            if (!$process->isSuccessful()) {
                throw new ProcessFailedException($process);
            }

            // Lo script Python ora ritorna il percorso *relativo* del file di output (relativo alla working directory)
            $outputRelativePath = trim($process->getOutput());

            // Ottieni il percorso alla directory 'app' e risali alla root del progetto
            $appPath = app_path(); // Es: .../backend/app
            // Risali due livelli: da app/ a backend/ a domoTek/
            $projectRoot = dirname(dirname($appPath));

            // Costruisci il percorso assoluto al file di output combinando la root del progetto con il percorso relativo
            $outputFilePath = $projectRoot . '/' . $outputRelativePath;

            // Log the output file path for debugging
            Log::info('Output file path (using app_path + relative): ' . $outputFilePath);

            // Verifica se il file di output esiste e è leggibile
            if (!file_exists($outputFilePath) || !is_readable($outputFilePath)) {
                 // Include il percorso assoluto nel messaggio di errore per debugging
                 throw new \Exception('File di output scansione non trovato o non leggibile: ' . $outputFilePath);
            }

            // Leggi il contenuto del file di output
            $fileContent = file_get_contents($outputFilePath);

            // Decodifica il contenuto JSON
            $scanResults = json_decode($fileContent, true);

            // Controlla se la decodifica JSON è avvenuta con successo
            if (json_last_error() !== JSON_ERROR_NONE) {
                throw new \Exception('Errore nella decodifica del file JSON di output: ' . json_last_error_msg());
            }

            // Opzionale: rimuovi il file di output dopo averlo letto
            // unlink($outputFilePath);

            // Restituisce i risultati della scansione al frontend
            return response()->json([
                'status' => 'success',
                'protocol' => $protocol,
                'results' => $scanResults,
            ]);
        } catch (ProcessFailedException $exception) {
            // Gestisce gli errori nell'esecuzione dello script Python
             Log::error('ProcessFailedException during scan', [
                'message' => $exception->getMessage(),
                'errorOutput' => $process->getErrorOutput(),
                'command' => $process->getCommandLine(),
                'exitCode' => $process->getExitCode(),
            ]);

            return response()->json([
                'status' => 'error',
                'protocol' => $protocol,
                'message' => 'Errore durante l\'esecuzione dello scanner per il protocollo ' . $protocol,
                'details' => $exception->getMessage(),
                'errorOutput' => $process->getErrorOutput(),
                'executedCommand' => $process->getCommandLine(),
            ], 500);
        } catch (\Exception $e) {
             // Gestisce altri tipi di errori (es. validazione, file not found, json decode error)
              Log::error('Exception during scan handling', [
                 'message' => $e->getMessage(),
                 'protocol' => $protocol,
             ]);

             return response()->json([
                 'status' => 'error',
                 'message' => 'Errore nella gestione dell\'output della scansione',
                 'details' => $e->getMessage(),
                 'protocol' => $protocol,
             ], 500);
        }
    }
}
