// --- MY FACEBOX AI FILTER & CHATBOT COMBINED SCRIPT (100% Backend Ready) ---

// 1. නරක වචන ලැයිස්තුව (Blacklist)
const badWords = ['badword1', 'badword2', 'අසභ්‍යවචනයක්']; // අවශ්‍ය නරක වචන මෙහි යොදන්න

// 2. අන්තර්ගතය ආරක්ෂිතදැයි පරීක්ෂා කිරීම (Auto Comment & Post Filter)
function isContentSafe(text) {
    if (!text) return true;
    const lowerText = text.toLowerCase();
    for (let word of badWords) {
        if (lowerText.includes(word)) {
            return false; // නරක වචන අඩංගු නම් False දෙයි
        }
    }
    return true; // ආරක්ෂිතයි
}

// 3. AI Chatbot ස්වයංක්‍රීය පිළිතුරු සහ ආරක්ෂක පරීක්ෂාව
function getAIChatResponse(userMessage) {
    if (!userMessage) return 'කරුණාකර පණිවිඩයක් ටයිප් කරන්න.';
    
    // චැට් එකට එන පණිවිඩවලත් නරක වචන තියෙනවද බලලා ෆිල්ටර් කිරීම
    if (!isContentSafe(userMessage)) {
        return '⚠️ කණගාටුයි, ඔබගේ පණිවිඩයේ නුසුදුසු වචන අඩංගු වන බැවින් මට එයට පිළිතුරු දිය නොහැක.';
    }

    const msg = userMessage.toLowerCase();
    
    // Smart AI Logic පිළිතුරු සැපයීම
    if (msg.includes('hi') || msg.includes('hello') || msg.includes('ආයුබෝවන්')) {
        return 'ආයුබෝවන්! myfacebox වෙත සාදරයෙන් පිළිගනිමු. මම ඔබේ AI සහායකයා වෙමි. ඔබට මගෙන් කුමන උදව්වක්ද අවශ්‍ය?';
    } else if (msg.includes('app') || msg.includes('yedm')) {
        return 'මෙය ජාත්‍යන්තර මට්ටමින් සකස් කළ myfacebox නවීන සමාජ ජාල යෙදුමකි! 🔥';
    } else {
        return 'ඔබගේ පණිවිඩය ලැබුණි! අපි මේ පිළිබඳව වැඩිදුර පරීක්ෂා කරමින් සිටිමු.';
    }
}

// 4. කමෙන්ට් හෝ පෝස්ට් එකක් සර්වර් එක හරහා වැලිඩේට් කර ක්‍රියාත්මක කිරීම (Backend API Compatible)
function validateAndProcessComment(postId, commentText) {
    if (!isContentSafe(commentText)) {
        return {
            success: false,
            message: '⚠️ අනතුරු ඇඟවීමයි: මෙම කමෙන්ට් එකෙහි නුසුදුසු වචන අඩංගු වන බැවින් එය පළ කළ නොහැක!'
        };
    }
    
    return {
        success: true,
        message: 'Comment is safe and posted successfully!'
    };
}

