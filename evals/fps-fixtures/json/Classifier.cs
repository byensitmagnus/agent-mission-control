using System.Text.Json;

public static class Classifier
{
    public static string Classify(string json)
    {
        using var document = JsonDocument.Parse(json);
        var root = document.RootElement;
        if (root.GetProperty("status").GetString() != "ok") return "FAIL";
        return root.GetProperty("failedCount").TryGetInt32(out var failedCount) && failedCount == 0
            ? "APPLIED"
            : "FAIL";
    }
}
