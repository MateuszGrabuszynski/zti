//
//  RequestData.swift
//  ZTI_mobile_app
//
//  Created by Adam Linke on 27/11/2018.
//  Copyright © 2018 Adam Linke. All rights reserved.
//

import Foundation
import Alamofire


struct RequestData {
    let prefixXsd = "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
    let prefixNif = "@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> ."
    let prefixDbpedia = "@prefix dbpedia: <http://dbpedia.org/resource/> ."
    let prefixItsrdf = "@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> ."
    
    let example: String //"<http://example.com/example-task1#char=0,146>"
    let a = "a                     nif:RFC5147String , nif:String , nif:Context ;"
    let nifBeginIndex: String
    let nifEndIndex: String
    let nifIsString: String
    
    init(text: String) {
        
        example = "<http://example.com/example-task1#char=0,\(text.count)>"
        nifBeginIndex = "nif:beginIndex        \"0\"^^xsd:nonNegativeInteger ;\"" //0\"^^xsd:nonNegativeInteger ;\"
        nifEndIndex = "nif:endIndex          \"\(text.count)\"^^xsd:nonNegativeInteger ;\""
        nifIsString = "nif:isString         \"\(text)\"@en ."
    }
    func request() -> String {
        let fullMessage = ("\(prefixXsd)\n\(prefixNif)\n\(prefixDbpedia)\n\(prefixItsrdf)\n\(example)\n\(a)\n\(nifBeginIndex)\n\(nifEndIndex)\n\(nifIsString)")
        return fullMessage
    }
    func returnAsDict() -> [String: Any] {
        let dict = ["prefixXsd": prefixXsd, "prefixNif": prefixNif, "prefixDbpedia": prefixDbpedia, "prefixItsrdf": prefixItsrdf, "example": example, "a": a, "nifBeginIndex": nifBeginIndex, "nifEndIndex": nifEndIndex, "nifIsString": nifIsString]
        return dict
    }
    
//    func post() {
//        let parameters = "\(prefixXsd)\n\(prefixNif)\n\(prefixDbpedia)\n\(prefixItsrdf)\n\(example)\n\(a)\n\(nifBeginIndex)\n\(nifEndIndex)\n\(nifIsString)"
//
//        Alamofire.request("https://httpbin.org/post", method: .post, parameters: parameters)
//    }
}
