#!/usr/bin/env python3
"""
Synapse Brain App v22 - 4-AI 코드 검증 스크립트
Gemini, Grok, OpenAI, Anthropic API를 활용하여 코드 품질 검증
"""

import os
import json
import time
import requests
import re

# API 키 로드
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
XAI_API_KEY = os.environ.get('XAI_API_KEY', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# 검증용 코드 로드
with open('/home/ubuntu/braindump/ai_review_summary.js', encoding='utf-8') as f:
    code_summary = f.read()[:7000]  # 토큰 제한

# 검증 프롬프트
REVIEW_PROMPT = f"""다음은 Synapse Brain App v22의 아카이브(Archive) 탭 핵심 JavaScript 함수들입니다.
코드를 검토하고 다음 항목을 100점 만점으로 평가해주세요:

1. bug_risk (0=버그없음~100=심각): 잠재적 버그나 엣지케이스
2. code_quality (0~100): 가독성, 유지보수성, 효율성
3. completeness (0~100): stub/미구현 함수 여부
4. overall_score (0~100): 종합 점수
5. bugs_found: 발견된 버그 목록 (최대 3개, 한국어)
6. improvements: 개선 제안 (최대 3개, 한국어)
7. summary: 한 줄 요약 (한국어)

반드시 JSON 형식으로만 응답하세요.

코드:
```javascript
{code_summary}
```"""

results = {}

def parse_json_result(text, ai_name):
    """JSON 결과 파싱"""
    text = text.strip()
    # 마크다운 코드블록 제거
    text = re.sub(r'```(?:json)?\n?', '', text).strip()
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError as e:
            print(f"  ⚠️  {ai_name}: JSON 파싱 오류 - {e}")
            return {'raw': text[:200], 'overall_score': None}
    return {'raw': text[:200], 'overall_score': None}

def print_result(ai_name, result):
    """결과 출력"""
    if 'error' in result:
        print(f"  ❌ {ai_name}: {result['error'][:100]}")
        return
    score = result.get('overall_score', '?')
    print(f"  ✅ {ai_name}: 전체 {score}점")
    print(f"     버그위험: {result.get('bug_risk','?')}, 품질: {result.get('code_quality','?')}, 완성도: {result.get('completeness','?')}")
    print(f"     요약: {result.get('summary', '')}")
    bugs = result.get('bugs_found', [])
    if bugs:
        print(f"     발견된 버그: {' | '.join(str(b) for b in bugs[:3])}")
    improvements = result.get('improvements', [])
    if improvements:
        print(f"     개선 제안: {' | '.join(str(i) for i in improvements[:3])}")

# ─────────────────────────────────────────────────────────
# 1. Gemini 검증 (google-genai SDK 사용)
# ─────────────────────────────────────────────────────────
def review_with_gemini():
    print("\n[1/4] Gemini 검증 시작...")
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=REVIEW_PROMPT,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=1024,
            )
        )
        result = parse_json_result(response.text, 'Gemini')
        print_result('Gemini', result)
        return result
    except Exception as e:
        result = {'error': str(e)[:200]}
        print_result('Gemini', result)
        return result

# ─────────────────────────────────────────────────────────
# 2. Grok 검증
# ─────────────────────────────────────────────────────────
def review_with_grok():
    print("\n[2/4] Grok 검증 시작...")
    try:
        headers = {
            'Authorization': f'Bearer {XAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'grok-3-mini',
            'messages': [
                {'role': 'system', 'content': 'You are a senior JavaScript code reviewer. Respond with valid JSON only.'},
                {'role': 'user', 'content': REVIEW_PROMPT}
            ],
            'temperature': 0.1,
            'max_tokens': 1024,
        }
        r = requests.post('https://api.x.ai/v1/chat/completions', headers=headers, json=payload, timeout=90)
        r.raise_for_status()
        text = r.json()['choices'][0]['message']['content']
        result = parse_json_result(text, 'Grok')
        print_result('Grok', result)
        return result
    except Exception as e:
        result = {'error': str(e)[:200]}
        print_result('Grok', result)
        return result

# ─────────────────────────────────────────────────────────
# 3. OpenAI 검증 (OPENAI_API_BASE 사용)
# ─────────────────────────────────────────────────────────
def review_with_openai():
    print("\n[3/4] OpenAI 검증 시작...")
    try:
        # OPENAI_API_BASE가 /v1/responses로 끝나는 경우 처리
        base = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1/responses')
        # chat/completions 엔드포인트 구성
        if 'responses' in base:
            # responses API 사용
            endpoint = base.rstrip('/')
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            payload = {
                'model': 'gpt-4o-mini',
                'input': REVIEW_PROMPT,
                'max_output_tokens': 1024,
            }
            r = requests.post(endpoint, headers=headers, json=payload, timeout=90)
            r.raise_for_status()
            rj = r.json()
            # responses API 응답 형식
            text = rj.get('output', [{}])[0].get('content', [{}])[0].get('text', '') if rj.get('output') else rj.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            endpoint = base.rstrip('/') + '/chat/completions'
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            payload = {
                'model': 'gpt-4o-mini',
                'messages': [
                    {'role': 'system', 'content': 'You are a senior JavaScript code reviewer. Respond with valid JSON only.'},
                    {'role': 'user', 'content': REVIEW_PROMPT}
                ],
                'temperature': 0.1,
                'max_tokens': 1024,
                'response_format': {'type': 'json_object'}
            }
            r = requests.post(endpoint, headers=headers, json=payload, timeout=90)
            r.raise_for_status()
            text = r.json()['choices'][0]['message']['content']

        result = parse_json_result(text, 'OpenAI')
        print_result('OpenAI', result)
        return result
    except Exception as e:
        result = {'error': str(e)[:200]}
        print_result('OpenAI', result)
        return result

# ─────────────────────────────────────────────────────────
# 4. Anthropic Claude 검증
# ─────────────────────────────────────────────────────────
def review_with_claude():
    print("\n[4/4] Claude 검증 시작...")
    try:
        headers = {
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'claude-3-5-haiku-20241022',
            'max_tokens': 1024,
            'messages': [
                {'role': 'user', 'content': REVIEW_PROMPT + '\n\nIMPORTANT: Respond with valid JSON only, no markdown code blocks.'}
            ]
        }
        r = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=payload, timeout=90)
        r.raise_for_status()
        text = r.json()['content'][0]['text']
        result = parse_json_result(text, 'Claude')
        print_result('Claude', result)
        return result
    except Exception as e:
        result = {'error': str(e)[:200]}
        print_result('Claude', result)
        return result

# ─────────────────────────────────────────────────────────
# 실행
# ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("Synapse Brain App v22 - 4-AI 코드 검증")
    print("=" * 60)

    results['gemini'] = review_with_gemini()
    time.sleep(2)
    results['grok'] = review_with_grok()
    time.sleep(2)
    results['openai'] = review_with_openai()
    time.sleep(2)
    results['claude'] = review_with_claude()

    # 종합 점수 계산
    print("\n" + "=" * 60)
    print("4-AI 종합 검증 결과")
    print("=" * 60)

    scores = []
    for ai_name, result in results.items():
        score = result.get('overall_score')
        if isinstance(score, (int, float)):
            scores.append(score)
            print(f"  {ai_name.upper():10s}: {score:5.1f}점")
        else:
            print(f"  {ai_name.upper():10s}: 점수 없음 (오류)")

    if scores:
        avg = sum(scores) / len(scores)
        print(f"\n  ─────────────────────")
        print(f"  평균 점수: {avg:.1f}점 / 100점")
        if avg >= 90:
            verdict = "✅ 배포 승인 (90점 이상)"
        elif avg >= 75:
            verdict = "⚠️  조건부 승인 (75-89점) - 개선 권장"
        else:
            verdict = "❌ 재검토 필요 (75점 미만)"
        print(f"  {verdict}")

    # 모든 AI의 개선 제안 종합
    all_improvements = []
    for ai_name, result in results.items():
        for imp in result.get('improvements', []):
            if imp and str(imp) not in all_improvements:
                all_improvements.append(str(imp))

    if all_improvements:
        print(f"\n  종합 개선 제안 ({len(all_improvements)}개):")
        for i, imp in enumerate(all_improvements[:8], 1):
            print(f"  {i}. {imp}")

    # 결과 저장
    with open('/home/ubuntu/braindump/ai_review_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'results': results,
            'scores': scores,
            'average': sum(scores)/len(scores) if scores else None,
            'improvements': all_improvements
        }, f, ensure_ascii=False, indent=2)
    print("\n결과 저장: ai_review_results.json")
