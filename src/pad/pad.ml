open Http_types
open List
open Cryptokit

let newdoc req outchan : string =
  try
    let message = req#body in
    let rng = Random.device_rng "/dev/urandom" in
    let rstr = (transform_string (Hexa.encode ()) (Random.string rng 20)) in
    let oc = open_out (rstr ^ ".md") in
    output_string oc message;
    "/" ^ rstr
  with
    Not_found -> "NOPE"


let readdoc req outchan : unit =
  let splitted = String.split_on_char '/' req#path in
  if (length splitted) == 3 && (String.equal (nth splitted 2) "download")
  then begin
      let ch = open_in ((nth splitted 1) ^ ".md") in
      let filecontent = really_input_string ch (in_channel_length ch) in
      Http_daemon.respond ~code:(`Code 200) ~body: filecontent outchan
    end
  else begin
      let fileparts = String.split_on_char '.' (nth splitted 1) in
      if (length fileparts) > 1 && String.equal (nth fileparts 1) "md"
      then begin
          let ch = open_in (nth splitted 1) in
          let filecontent = really_input_string ch (in_channel_length ch) in
          Http_daemon.respond ~code:(`Code 200) ~body: filecontent outchan
        end
      else
        Http_daemon.respond ~code:(`Code 302) ~headers:[("Location", "/#!" ^ (nth splitted 1) ^ ".md" )] outchan
    end




let dispatch index (req : Http_types.request) (outchan : out_channel) : unit =
  (* Forking server and OCaml doesn't re-init its RNG on fork *)

  (*
  let authh = req#header "Authentication" in
  let result = exists (fun pkey -> FaustAuthenticate.schnorrValidate pkey pp authh) pkeylist in
   *)
  let result = true in


  (match req#path with
   | "/new"      -> Http_daemon.respond ~code:(`Code 302) ~headers:[("Location", (newdoc req outchan) )] outchan
   | "/"          -> Http_daemon.respond ~code:(`Code 200) ~body: index outchan
   | bad_request -> readdoc req outchan
  )


let _ =
  let ch = open_in "../pad/index.html" in
  let index = really_input_string ch (in_channel_length ch) in

  let spec =
    { Http_daemon.default_spec with
      address = "127.0.0.66";
      callback = dispatch index;
      port = 9999;
    }
  in
  Http_daemon.main spec
