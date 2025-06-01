<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\Api\NetworkScanController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Qui vanno tutte le rotte API con prefisso /api automatico
| Il middleware di default è 'api' (configurato in bootstrap/app.php)
|
*/

Route::middleware('auth.api')->group(function () {
    Route::get('/user', [AuthController::class, 'user']);
    Route::post('/logout', [AuthController::class, 'logout']);
});


Route::post('/login', [AuthController::class, 'login']);
Route::post('/register', [AuthController::class, 'register']);

// Nuova rotta per avviare la scansione della rete
Route::post('/scan-network', [NetworkScanController::class, 'scan']);