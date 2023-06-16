function decodeUplink(input) {
    var decoded = {
        msg: "" // Initalise decoded.msg as an empty string
    };
    
    for (var i = 0; i < input.bytes.length; i++){
        decoded.msg += String.fromCodePoint(input.bytes[i]);
    }
    
    return {
        data: decoded,
        warnings: [],
        errors: []
    };
}
  